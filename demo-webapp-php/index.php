<?php
/* Start session. */
session_start();

if (isset($_POST['email'])) {
    $_SESSION['email'] = $_POST['email'];
    $email = $_SESSION['email'];
} else if (isset($_SESSION['email'])) {
    $email = $_SESSION['email'];
} else {
    $email = '';
}
?>
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>ChatCPT - BrokenAI</title>
    <link rel="stylesheet" href="./style.css">
    <link rel="icon" href="./favicon.png" type="image/x-icon">
  </head>
  <body>
    <div id="container">
        <form action="" method="POST">
        <div id="chatcpt">
            <center><img src="chatcpt.png"></center>
        </div>
        <div id="login">
            <label id="email_lbl" for="email_inp">&nbsp;Email address&nbsp;</label>
            <div id="email">
                <input class="login_inp" type="text" id="email_inp" name="email" value="<?php echo(htmlentities($email)); ?>"/>
            </div>
            <label id="password_lbl" for="email_inp">&nbsp;Password&nbsp;</label>
            <div id="password">
                <input class="login_inp" type="password" id="passwd_inp" name="password"/>
            </div>
            <input type="submit" id="login" value="Continue"></input>
            <div id="signup">
                <center>
                Don't have an account ? <a href="#">Sign up</a>
                </center>
            </div>
        </div>
        </form>
    </div>
  </body>
</html>
