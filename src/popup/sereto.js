if (typeof browser === "undefined") {
  var browser = chrome;
}

function showCookiesForTab(tabs) {
  // get the first tab object in the array
  const tab = tabs[0];

  if (!tab || !tab.url) {
    console.error('No valid tab found');
    return;
  }

  // get all cookies in the domain
  const hostname = new URL(tab.url).hostname;
  const parts = hostname.split('.');
  const domain = parts.length > 2 ? parts.slice(1).join('.') : hostname;
  const gettingAllCookies = browser.cookies.getAll({domain: domain});
  gettingAllCookies.then((cookies) => {

    // set the header of the panel
    let activeTabUrl = document.getElementById('header-title');
    activeTabUrl.innerText = `Cookies at:\n\t${tab.title}\n\t${tab.url}`;
    const cookieTextArea = document.getElementById("textarea-cookies");

    if (cookies.length > 0) {
      // sort cookies by name
      cookies.sort((a, b) => a.name.localeCompare(b.name));
      // insert cookies into the textarea
      let output = '';
      const selectedOption = document.querySelector('input[name="cookie-list"]:checked').value;
      if (selectedOption === 'flags') {
        output = getCookiesFlags(cookies);
      } else if (selectedOption === 'parent-domain') {
        output = getCookiesParentDomain(cookies);
      } else if (selectedOption === 'persistent') {
        output = getCookiesPersistent(cookies);
      }
      cookieTextArea.value = output;
    } else {
      cookieTextArea.value = "No cookies in this tab.";
    }
  });
}

function getCookiesFlags(cookies) {
  let output = '[variables]\ncookies = [\n';
  let secure = true;
  let httpOnly = true;
  let sameSite = true;

  for (const cookie of cookies) {
    secure = secure && cookie.secure;
    httpOnly = httpOnly && cookie.httpOnly;
    sameSite = sameSite && cookie.sameSite !== "no_restriction";
    output += `    { name = "${cookie.name}", http_only = "${cookie.httpOnly}", secure = "${cookie.secure}", same_site = "${capitalizeFirstLetter(cookie.sameSite)}" },\n`;
  }
  output += ']\n';
  output = output.replace(/true/gi, "yes");
  output = output.replace(/false/gi, "no");
  output += `secure = ${secure}\nhttp_only = ${httpOnly}\nsame_site = ${sameSite}\n`;
  // Firefox uses "no_restriction" for None
  output = output.replace(/no_restriction/gi, "None");
  // Cookies behave as Lax by default
  output = output.replace(/unspecified/gi, "Lax");
  return output;
}

function getCookiesParentDomain(cookies) {
  let output = '[variables]\ncookies = [\n';

  for (const cookie of cookies) {
    if (cookie.domain.startsWith('.')) {
      output += `    "${cookie.name}",\n`;
      domain = cookie.domain;
    }
  }
  output += `]\ndomain = "${domain}"\n`;
  return output;
}

function getCookiesPersistent(cookies) {
  let output = '[variables]\ncookies = [\n';

  for (const cookie of cookies) {
    if (cookie.expirationDate && cookie.expirationDate > Date.now() / 1000) {
      // recalculate lifespan in days
      const currentTime = Math.floor(Date.now() / 1000);
      const lifespanSeconds = cookie.expirationDate - currentTime;
      let lifespan = `${lifespanSeconds} seconds`;
      const days = Math.floor(lifespanSeconds / 86400);
      const hours = Math.floor(lifespanSeconds / 3600);
      const minutes = Math.floor(lifespanSeconds / 60);
      if (days > 0) {
        lifespan = `${days} days`;
      } else if (hours > 0) {
        lifespan = `${hours} hours`;
      } else if (minutes > 0) {
        lifespan = `${minutes} minutes`;
      }
      output += `    { name = "${cookie.name}", lifespan = "${lifespan}" },\n`;
    }
  }
  output += ']\n';
  return output;
}

async function copyCookies() {
  try {
    const copyText = document.querySelector("#textarea-cookies");
    copyText.select();
    await navigator.clipboard.writeText(copyText.value);
  } catch (err) {
    console.error('Failed to copy: ', err);
  }
}

// get active tab to run an callback function
// sends to the callback an array of tab objects
function getActiveTab() {
  return browser.tabs.query({currentWindow: true, active: true});
}

// capitalize first letter of a string
function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

function updateCookieDisplay() {
  getActiveTab().then(showCookiesForTab);
}

// add event listener for the copy button for cookies
document.querySelector("#copy-cookies").addEventListener("click", copyCookies);

// add event listener for the radio buttons
const radioButtons = document.querySelectorAll('input[name="cookie-list"]');
radioButtons.forEach(radio => {
  radio.addEventListener('change', updateCookieDisplay);
});

updateCookieDisplay();
