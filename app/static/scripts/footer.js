var isToggled = false;
function toggleLanguage(){
  $('#footer_toggle').animate({'bottom': (isToggled ? '30px' : '70px')});
  isToggled = !isToggled;
  $('#language_footer').slideToggle();
  if(isToggled)
    $('#language_footer').transition('jiggle'); //or pulse
}

// nothing to see here
$(document).ready(function() {
  let highScore = Cookies.get('highScore');
  if(highScore == null){
    Cookies.set('highScore', 99999, { expires: 365, sameSite: 'secure' });
  }
  let start = performance.now();
  let end = 0;
  let konamiCode = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65, 13].reverse();
  let keysToPress = konamiCode.slice();
  document.onkeydown = checkKey;
  function checkKey(e) {  
    e = e || window.event;
    if(e.keyCode === keysToPress[keysToPress.length - 1]){
      if(keysToPress.length == konamiCode.length){
        start = performance.now();
      }
      keysToPress.pop();
      if (keysToPress.length === 0){
        end = performance.now();
        let totalTime = (end - start)/1000;
        if(totalTime < highScore || highScore == null){
          highScore = totalTime;
          Cookies.set('highScore', highScore, { expires: 365 });
          alert('New highscore! You took ' + totalTime + ' seconds to type in the Konami Code');
          activateConfetti();
        }
        else{
          alert('You took ' + totalTime + ' seconds to type in the Konami Code.\nHighscore: ' + highScore);
        }
        keysToPress = konamiCode.slice();
      }
    }
    else{
      keysToPress = konamiCode.slice();
    }
  }
});

async function activateConfetti() {
  confetti.start();
  await new Promise(r => setTimeout(r, 3000));
  confetti.stop();
}