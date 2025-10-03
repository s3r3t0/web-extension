if (typeof browser === "undefined") {
  var browser = chrome;
}

function showCookiesForTab(tabs) {
  // get the first tab object in the array
  let tab = tabs.pop();

  // get all cookies in the domain
  var gettingAllCookies = browser.cookies.getAll({url: tab.url});
  gettingAllCookies.then((cookies) => {

    // set the header of the panel
    var activeTabUrl = document.getElementById('header-title');
    var text = document.createTextNode("Cookies at: " + tab.title);
    var cookieTextArea = document.getElementById("textarea-cookies");
    activeTabUrl.appendChild(text);

    if (cookies.length > 0) {
      // sort cookies by name
      cookies.sort((a, b) => a.name.localeCompare(b.name));
      // insert cookies into the textarea
      cookieTextArea.value += '[variables]\ncookies = [\n';
      secure = true;
      httpOnly = true;
      sameSite = true;
      for (let cookie of cookies) {
        secure = secure && cookie.secure;
        httpOnly = httpOnly && cookie.httpOnly;
        sameSite = sameSite && cookie.sameSite !== "no_restriction";
        cookieTextArea.value += '    { name = "' + cookie.name + '", http_only = "' + cookie.httpOnly + '", secure = "' + cookie.secure + '", same_site = "' + capitalizeFirstLetter(cookie.sameSite) + '" },\n';
      }
      cookieTextArea.value = cookieTextArea.value.replace(/true/gi, "yes");
      cookieTextArea.value = cookieTextArea.value.replace(/false/gi, "no");
      cookieTextArea.value += ']\nsecure = ' + secure + '\nhttp_only = ' + httpOnly + '\nsame_site = ' + sameSite + '\n';
      cookieTextArea.value = cookieTextArea.value.replace(/no_restriction/gi, "None");
    } else {
      cookieTextArea.value = "No cookies in this tab.";
    }
  });
}

function copyCookies() {
  var copyText = document.querySelector("#textarea-cookies");
  copyText.select();
  document.execCommand("copy");
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

// add event listener for the copy button for cookies
document.querySelector("#copy-cookies").addEventListener("click", copyCookies);

getActiveTab().then(showCookiesForTab);
