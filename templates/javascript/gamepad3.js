  //connect gamepad from window
  
  window.addEventListener("gamepadconnected", function(e) {
    console.log("Gamepad connected at index %d: %s. %d buttons, %d axes.",
      e.gamepad.index, e.gamepad.id,
      e.gamepad.buttons.length, e.gamepad.axes.length);
  });
  //set controller as gp
  var gp = navigator.getGamepads()[0];
  //disconnect gamepad from window
  window.addEventListener("gamepaddisconnected", function(e) {
    console.log("Gamepad disconnected from index %d: %s",
      e.gamepad.index, e.gamepad.id);
  });
  //apply Deadzone so no motor running when at rest
  var applyDeadzone = function(number, threshold){
    percentage = (Math.abs(number) - threshold) / (1 - threshold);
    if(percentage < 0)
      percentage = 0;
    return percentage * (number > 0 ? 1 : -1);
  }
  //runs python script in app.py
  var latch_tread = false;
  var latch_turret = false;
  let toggle_mode = false;

  function toggle() {
    toggle_mode = !toggle_mode;
  }

  function tread_mode() {
   
    gp = navigator.getGamepads()[0];

    if (gp.buttons[14].pressed) {
      toggle();
    }

    shutdown = gp.buttons[16].pressed;

    joystick1 = applyDeadzone(gp.axes[1], 0.15);
    joystick2 = applyDeadzone(gp.axes[3], 0.15);

    frontLeftFlipperUp = gp.buttons[4].pressed;
    frontLeftFlipperDown = gp.buttons[6].pressed;

    frontRightFlipperUp = gp.buttons[5].pressed;
    frontRightFlipperDown = gp.buttons[7].pressed;

    backLeftFlipperUp = gp.buttons[13].pressed;
    backLeftFlipperDown = gp.buttons[12].pressed;

    backRightFlipperUp = gp.buttons[0].pressed;
    backRightFlipperDown = gp.buttons[3].pressed;
    if(frontLeftFlipperUp || frontLeftFlipperDown || frontRightFlipperUp || frontRightFlipperDown || backLeftFlipperUp || backLeftFlipperDown || backRightFlipperUp || backRightFlipperDown || joystick1 != 0 || joystick2 != 0 || shutdown) {
    
    $.ajax({
      url: "{{ url_for('mode_one') }}",
      type: 'POST',
      data: {'shutdown': shutdown,'joystick1': joystick1, 'joystick2': joystick2, 'frontLeftFlipperUp': frontLeftFlipperUp, 'frontLeftFlipperDown': frontLeftFlipperDown, 'frontRightFlipperUp': frontRightFlipperUp, 'frontRightFlipperDown': frontRightFlipperDown, 'backLeftFlipperUp': backLeftFlipperUp, 'backLeftFlipperDown': backLeftFlipperDown, 'backRightFlipperUp': backRightFlipperUp, 'backRightFlipperDown': backRightFlipperDown},
      success: function(response) {
        console.log("Tread Mode Sent");

      }
    });
    latch_tread = true;
    } 
    console.log(latch_tread);
    if (latch_tread == true && frontLeftFlipperUp == false && frontLeftFlipperDown == false && frontRightFlipperUp == false && frontRightFlipperDown == false && backLeftFlipperUp == false && backLeftFlipperDown == false && backRightFlipperUp == false && backRightFlipperDown == false && joystick1 == 0 && joystick2 == 0 && shutdown == false) {
      $.ajax({
        url: "{{ url_for('mode_one') }}",
        type: 'POST',
        data: {'shutdown': shutdown,'joystick1': joystick1, 'joystick2': joystick2, 'frontLeftFlipperUp': frontLeftFlipperUp, 'frontLeftFlipperDown': frontLeftFlipperDown, 'frontRightFlipperUp': frontRightFlipperUp, 'frontRightFlipperDown': frontRightFlipperDown, 'backLeftFlipperUp': backLeftFlipperUp, 'backLeftFlipperDown': backLeftFlipperDown, 'backRightFlipperUp': backRightFlipperUp, 'backRightFlipperDown': backRightFlipperDown},
        success: function(response) {
          console.log("Tread Mode Sent");
        }
      });
      
      latch_tread = false;
    }
    console.log(latch_tread);
    }

  function turret_mode() {

    gp = navigator.getGamepads()[0];

    if (gp.buttons[14].pressed) {
      toggle();
    }

    shutdown2 = gp.buttons[16].pressed;

    shoulderControls = applyDeadzone(gp.axes[1], 0.25);
    elbowControls = applyDeadzone(gp.axes[3], 0.25);

    turretControls = applyDeadzone(gp.axes[0], 0.25);
    wristControls = applyDeadzone(gp.axes[2], 0.25);

    clawOpen = gp.buttons[6].value;
    clawClose = gp.buttons[7].value;

    $.ajax({
      url: "{{ url_for('mode_two') }}",
      type: 'POST',
      data: {'shutdown2': shutdown2,'shoulderControls': shoulderControls, 'elbowControls': elbowControls, 'turretControls': turretControls, 'wristControls': wristControls, 'clawOpen': clawOpen, 'clawClose': clawClose},
      success: function(response) {
        console.log("Turret Mode Sent");
      }
    });
    }

    function run() {
        if (!toggle_mode) {
        tread_mode();
        } else {
        turret_mode();
        }
    }
    setInterval(run, 100);