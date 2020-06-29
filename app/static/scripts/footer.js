var isToggled = false;
function toggleLanguage(){
  $('#footer_toggle').animate({'bottom': (isToggled ? '30px' : '70px')});
  isToggled = !isToggled;
  $('#language_footer').slideToggle();
  if(isToggled)
    $('#language_footer').transition('jiggle'); //or pulse
}

// nothing to see here
let konamiCode = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65, 13].reverse();
let keysToPress = konamiCode.slice();
document.onkeydown = checkKey;
function checkKey(e) {  
  e = e || window.event;
  if(e.keyCode == keysToPress[keysToPress.length - 1]){
    keysToPress.pop();
    if (keysToPress.length == 0){
      confetti.toggle();
      keysToPress = konamiCode.slice();
    }
  }
  else{
    keysToPress = konamiCode.slice();
  }
}