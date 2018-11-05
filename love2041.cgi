#!/usr/bin/perl -w

# written by andrewt@cse.unsw.edu.au September 2013
# as a starting point for COMP2041/9041 assignment 2
# http://cgi.cse.unsw.edu.au/~cs2041/assignments/LOVE2041/
# edited by David Chacon October 2014

#credit to css boostrap for design of the page

use CGI qw/:all/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use CGI::Cookie;
use Data::Dumper;  
use List::Util qw/min max/;

warningsToBrowser(1);

%cookies = CGI::Cookie->fetch;

if (defined $cookies{'x'} && $cookies{'x'}->value =~ /[A-Za-z]+/){
   $item = $cookies{'x'}->value;
   @data = split ('=', $item);
   $username = $data[0];
   $password = $data[1];
   if ($ENV{'QUERY_STRING'} eq "page=Home0"){
      $cookie = CGI::Cookie->new(-name=>$username, -value=>'', -path=>'/', -expires=>'-1d');
      $password = "";
      undef $username;
      undef $password;
      undef $item;
      delete $cookies{'x'};
   } else {
      $cookie = CGI::Cookie->new(-name=>$username, -value=>$password, -path=>'/', -expires=>'4d');
   }
}

if ($correctPassword eq $password && defined param('username') && defined param('password')){
   $cookie = CGI::Cookie->new(-name=>param('username'), -value=>'yay', -path=>'/', -expires=>'4d'); 
}

# print start of HTML ASAP to assist debugging if there is an error in the script
print page_header();
print "<link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.0/css/bootstrap.min.css'>\n";
print navbar();

# some globals used through the script
$debug = 1;
$students_dir = "./students";
if (defined param('searchQuery')){
   if (defined $cookie){
         print search_users();
      } else {
         print needtologin_screen();
      }
} elsif (defined param('signup')){
   print account_creation_screen();
} elsif (length ($ENV{'QUERY_STRING'}) > 0){
   if ($ENV{'QUERY_STRING'} =~ /page=Browse/){
      if (defined $cookie){
         print browse_users();
      } else {
         print needtologin_screen();
      }
   } elsif ($ENV{'QUERY_STRING'} =~ /page=About$/){
      print about_us();
   } elsif ($ENV{'QUERY_STRING'} =~ /page=Home(0)?$/) {
      print home_screen();
   } elsif ($ENV{'QUERY_STRING'} =~ /user=[A-Za-z]+[0-9]*([A-Za-z]+[0-9]*)*/) {
      if (defined $cookie){
         print view_details();
      } else {
         print needtologin_screen();
      }
   } elsif ($ENV{'QUERY_STRING'} =~ /page=LogIn$/) {
      if (defined param('username') && defined param('password')){
         print check_password();         
      } else {
         print login_screen();
      }
   } elsif ($ENV{'QUERY_STRING'} =~ /page=check$/) {
      check_password();
   } elsif ($ENV{'QUERY_STRING'} =~ /page=SignUp$/) {
      print signup_screen();
   } elsif ($ENV{'QUERY_STRING'} =~ /page=ViewMatches$/) {
      print find_matches();
   } elsif ($ENV{'QUERY_STRING'} =~ /page=ViewProfile$/) {
      if (defined param('save')){
         save_file();
      } else {
         print view_profile();
      }
   } elsif ($ENV{'QUERY_STRING'} =~ /page=Upload$/) {
      print view_profile();
   } elsif ($ENV{'QUERY_STRING'} =~ /page=forgotPassword$/) {
      if (defined param('email')){
         check_email();
      } else {
         print forgotPassword_screen();
      }
   } else {
      print error_screen();
   }
} else {
   print home_screen();
}

print page_trailer();
exit 0;	

sub account_creation_screen {
   my $username = param('new_username');
   my $password = param('new_password');
   my $email = param('new_email');
   my $gender = param('new_gender');
   my $dob = param ('new_dob');
   my @students = glob("$students_dir/*");
   my $flag = 1;
   foreach $x (@students){
      @name = split('/', $x);
      if ($name[2] eq $username){
         $flag = 0;
      }
   }
   if ($flag == 0){
      print "<center><font size='5'<p>Sorry, that username is already taken, please try again.";
   } else {
      $directory = "./students/$username";
      print "<center><font size='5'<p>Success! Please check your email address for the confirmation link to get started!";
      mkdir $directory;
      open my $p, '>', "$directory/profile.txt" or die "can not open $directory/profile.txt: $!";
      open my $q, '>', "$directory/preferences.txt" or die "can not open $directory/preference.txt: $!";
      print $p "username:\n";
      print $p "\t$username\n";
      print $p "password:\n";
      print $p "\t$password\n";
      print $p "email:\n";
      print $p "\t$email\n";
      print $p "gender:\n";
      print $p "\t$gender\n";
      print $p "birthdate:\n";
      print $p "\t$dob";
      print $q "add preferences here!";
   }
   return; 
}

sub signup_screen {
   print '<div class="container-fluid">
            <div class="row">
                <div class="col-md-4"></div>
                <div class="col-md-4">
    

                    <center><h3>Sign Up</h3></center>
                <form role="form" method="post">
                    
                    <div class="input-group">
                      <span class="input-group-addon">Username</span>
                      <input type="text" class="form-control" name="new_username" placeholder="Username">
                    </div>

                    <br>

                    <div class="input-group">
                      <span class="input-group-addon">Password     </span>
                      <input type="password" class="form-control" name="new_password" placeholder="Password">
                    </div>

                    <br>

                    <div class="input-group">
                      <span class="input-group-addon">Email Address</span>
                      <input type="email" class="form-control" name="new_email" placeholder="Email Address">
                    </div>

                    <br>
                    
                    <div class="input-group">
                      <span class="input-group-addon">Gender       </span>
                      <select class="form-control" name="new_gender">
                            <option>Male</option>
                            <option>Female</option>
                            <option>Other</option>
                        </select>
                    </div>
                    
                    <br>
                    
                    <div class="input-group">
                      <span class="input-group-addon">D.O.B        </span>
                      <input type="date" class="form-control" name="new_dob" placeholder="Date of Birth">
                    </div>

                    <br>

                    <br>
                    <button class="btn btn-lg btn-primary btn-block" name="signup" type="submit">Sign Up</button>
                </form>
    

                </div>
                <div class="col-md-4"></div>
            </div>
        </div>';
   return;
}

sub home_screen {
   if (defined $username){
      print "<center><p><h3>Welcome back $username! Click on the above links to find the love of your life!</h3></p></center>";
   } else {
      print "<center><p><h3>Welcome to the LOVE2041 dating website! To get started, either sign up or log in.</h3></p></center>";      
   }
   
   return;
}

sub needtologin_screen {
   print "<center><p><h3>Sorry, you need to login to access this feature.</h3></p></center>";      
   return;
}

sub login_screen {
   print '<div class="container-fluid">
            <div class="row">
                <div class="col-md-4"></div>
                <div class="col-md-4">
    

                    <center><h3>Login</h3></center>
                <form role="form" method="post">
                    <div class="input-group">
                      <span class="input-group-addon">Username</span>
                      <input type="text" class="form-control" name="username" placeholder="Username">
                    </div>

                    <br>

                    <div class="input-group">
                      <span class="input-group-addon">Password&nbsp</span>
                      <input type="password" class="form-control" name="password" placeholder="Password">
                    </div>

                    <br>

                    <button class="btn btn-lg btn-primary btn-block" type="submit">Log in</button>
                </form>
    

                </div>
                <div class="col-md-4"></div>
            </div>
        </div>';
   print "<br>\n<font size='3'><center><a href='?page=forgotPassword'>Forgot Password?</a><center></font>";

   return;
}

sub save_file {
   my $student_to_show  = "$students_dir/$username";
	my $profile_filename = "$student_to_show/profile.txt";
   my $profile_picture = "$student_to_show/profile.jpg";
	open my $p, "$profile_filename" or die "can not open $profile_filename: $!";
   open my $q, "$student_to_show/preferences.txt" or die "can not open $profile_filename: $!";
   @profields = ();
   @preffields = ();
   
   foreach $thing (<$p>){
      if ($thing =~ /^[A-Za-z]/){
         push @profields, $thing;
      }
   }
   foreach $thing (<$q>){
      if ($thing =~ /^[A-Za-z]/){
         push @preffields, $thing;
      }
   }
   close $p;
   close $q;
   
   open my $p, '>', "$profile_filename" or die "can not open $profile_filename: $!";
   open my $q, '>', "$student_to_show/preferences.txt" or die "can not open $profile_filename: $!";
   
   #foreach $item (@preffields){
   #   print $q $item;
   #   print $q param("$item");
   #}
   #foreach $item (@profields){
   #   print $p $item;
   #   print $p param("$item");
   #}
   close $p;
   close $q;
   print view_profile();
 	return;
}

sub view_profile {
   my $student_to_show  = "$students_dir/$username";
	my $profile_filename = "$student_to_show/profile.txt";
   my $profile_picture = "$student_to_show/profile.jpg";
	open my $p, "$profile_filename" or die "can not open $profile_filename: $!";
   open my $q, "$student_to_show/preferences.txt" or die "can not open $profile_filename: $!";
	@file = <$p>;
   @pref = <$q>;

   print "<pre>\n";
   if (-e $profile_picture){
      print "<center><img src = $profile_picture><br></center>\n";
   } else {
      print "<p><center>Profile picture not given</center><br></p>";
   }
   print "<center>",filefield('file', 'profile.jpg'),"</center><br>\n"; 
   print '<center><a href="?page=Upload"><input type="button" value="Upload"></a></center><br>';

   $x = 0;
   print "<b><u>More about myself</b></u><br>";
   print textarea("MoreInfo","Enter more text about yourself",10,50),"<br>\n";
   while ($x <= $#file){
      if ($file[$x] =~ /^[A-Za-z]/){
         chomp ($file[$x]);
         print "<b><u>$file[$x]</u></b>\n";
      } else {
         $string = "";
         $fieldname = $file[$x-1];
         while ($file[$x] =~ /^\s/){
            $file[$x] =~ s/^\s*//;
            $string .= $file[$x];
            $x++;
         }
         print textarea($fieldname,$string,5,100),"<br>\n";
         $x--;
      }
      $x++;
   }
   print "</pre>";
	close $p;
   print "<p>Preferences</p>";
   print "<pre>";
   $x = 0;
   while ($x <= $#pref){
      if ($pref[$x] =~ /^[A-Za-z]/){
         chomp ($pref[$x]);
         print "<b><u>$pref[$x]</u></b>\n";
      } else {
         $string = "";
         $fieldname = $pref[$x-1];
         while ($pref[$x] =~ /^\s/){
            $pref[$x] =~ s/^\s*//;
            $string .= $pref[$x];
            $x++;
         }
         print textarea($fieldname,$string,5,100),"<br>\n";
         $x--;
      }
      $x++;
   }
   print "</pre>";
   close $q;
   print '<div class="container-fluid">
            <div class="row">
                <div class="col-md-4"></div>
                <div class="col-md-4">
                <form role="form" method="post">
                    <button class="btn btn-lg btn-primary btn-block" name="save" type="submit">Save</button>
                </form>
    

                </div>
                <div class="col-md-4"></div>
            </div>
        </div>';
	return;
}

sub forgotPassword_screen {
   print '<div class="container-fluid">
            <div class="row">
                <div class="col-md-4"></div>
                <div class="col-md-4">
    

                    <center><h3>Password Recovery</h3></center>
                    <center><font size=4><p>Please enter your email address so that an email can be sent off to you with your password.</p></font></center>
                <form role="form" method="post">
                    <div class="input-group">
                      <span class="input-group-addon">Username</span>
                      <input type="text" class="form-control" name="recoverUser" placeholder="Username">
                    </div>
                    
                    <br>
                    
                    <div class="input-group">
                      <span class="input-group-addon">Email</span>
                      <input type="text" class="form-control" name="email" placeholder="email@example.com">
                    </div>
                    
                    <br>

                    <button class="btn btn-lg btn-primary btn-block" type="submit">Send Password</button>
                </form>
    

                </div>
                <div class="col-md-4"></div>
            </div>
        </div>';
   return;
}

sub error_screen {
   print "<h3><center><p>Error: You have stumbled across a page that doesn't exist. Check the URL is valid, or click
               on of the links above to proceed.</p></center><h3>";
   return;
}

sub check_email {
   $username = param('recoverUser');
   $email = param('email');
   chomp $username;
   chomp $email;
   $username =~ s/\</&lt/;
   $username =~ s/\>/&gt/;
   $email =~ s/\</&lt/;
   $email =~ s/\>/&gt/;
   
   $directory = "$students_dir/$username/profile.txt";
   
   if (-e $directory){
      open FILE, "<$directory", or die "can't open file";
      @file = <FILE>;
      $x = 0;
      while ($x <= $#file){
         if ($file[$x] =~ /^email:/){
            $x++;
            chomp ($file[$x]);
            $file[$x] =~ s/\s//g;
            $correctEmail = $file[$x];
         }
         if ($file[$x] =~ /^password:/){
            $x++;
            chomp ($file[$x]);
            $file[$x] =~ s/\s//g;
            $userPassword = $file[$x];
         }
         $x++;
      }
      chomp $correctEmail;
      if ($email eq $correctEmail){
         print confirmation_screen();
      } else {
         print forgotPassword_screen();
         print "<center><p>Username and email do not match. Please try again.</p></center>\n"
      }
      close (FILE);
   } else {
      print forgotPassword_screen();
      print "<br><br>";
      print "<center><p>Username and email do not match. Please try again.</p></center>\n"
   }
   return;
}

sub confirmation_screen {
   print "<center><font size='4'><p>Success! Your password will be emailed to you. Please go there for your password</p></font></center>\n";
   $to = $email;
   $from = 'Love2041@customersupport.com';
   $subject = 'Password Recovery';
   $message = "Hi $username! We have recieved a password request from you. Your password it $userPassword. We hope you continute to enjoy Love2041!";
    
   open(MAIL, "|/usr/sbin/sendmail -t");
    
   # Email Header
   print MAIL "To: $to\n";
   print MAIL "From: $from\n";
   print MAIL "Subject: $subject\n\n";
   # Email Body
   print MAIL $message;

   close(MAIL);
   return;
}

sub check_password {
   $username = param('username');
   $password = param('password');
   chomp $username;
   chomp $password;
   $username =~ s/\</&lt/;
   $username =~ s/\>/&gt/;
   $password =~ s/\</&lt/;
   $password =~ s/\>/&gt/;
   
   $directory = "$students_dir/$username/profile.txt";
   
   if (-e $directory){
      open FILE, "<$directory", or die "can't open file";
      @file = <FILE>;
      $x = 0;
      while ($x <= $#file){
         if ($file[$x] =~ /^password:/){
            $x++;
            chomp ($file[$x]);
            $file[$x] =~ s/\s//g;
            $correctPassword = $file[$x];
         }
         $x++;
      }
      chomp $correctPassword;
      if ($correctPassword eq $password){
         print home_screen();
      } else {
         print login_screen();
         print "<center><p>Username and password do not match. Please try again.</p></center>\n"
      }
      close (FILE);
   } else {
      print login_screen();
      print "<br><br>";
      print "<center><p>Username and password do not match. Please try again.</p></center>\n"
   }
   return;
}

sub search_users {
   my $word = $ENV{'QUERY_STRING'};
   @vars = split ('=', $word);
   $word = $vars[1];
   $word =~ s/\</&lt/;
   $word =~ s/\>/&gt/;
   $n = 0; 
	my @students = glob("$students_dir/*");
   foreach $x (@students){
      if ($x =~ /$word/i){
         $n++;
      }
   }
   print "<center><h2>there are $n matches</h2></center>\n";

   print "<div class='col-md-3'>\n";
   print "<center>\n";
   $flag = 0;

   for $num (0..$#students) {
      my $student_to_show  = $students[$num];
      if ($student_to_show =~ /$word/i){
         if ($flag == 1){
            print "</div>\n<div class='col-md-3'>\n<center>\n";
         }
         
         my $profile_filename = "$student_to_show/profile.txt";
         my $profile_picture = "$student_to_show/profile.jpg";
         open my $p, "$profile_filename" or die "can not open $profile_filename: $!";
         @file = <$p>;
         $x = 0;
         while ($x <= $#file){
            if ($file[$x] =~ /^birthdate:/){
               $x++;
               chomp ($file[$x]);
               $file[$x] =~ s/\s//g;
               @dob = split('/',$file[$x]);
               if ($dob[0] =~ /^[1-9][0-9]{3}$/){
                  $age = 2014 - $dob[0];
               } elsif ($dob[1] =~ /^[1-9][0-9]{3}$/){
                  $age = 2014 - $dob[1];
               } else {
                  $age = 2014 - $dob[2];
               }
            }
            if ($file[$x] =~ /^username:/){
               $x++;
               chomp ($file[$x]);
               $file[$x] =~ s/\s//g;
               $username = $file[$x];
            }
            if ($file[$x] =~ /^gender:/){      
               $x++;
               chomp ($file[$x]);
               $file[$x] =~ s/\s//g;
               $gender = $file[$x];
            }
            $x++;
         }
         if (-e $profile_picture){
            print "<a href='?user=$username'><img src = $profile_picture></a><br>\n";
         } else {
            print "<a href='?user=$username'>Profile picture not given<br></a>";
         }
         print "<b>Username:</b> $username<br>\n";
         print "<b>Age:</b> $age<br>\n";
         print "<b>Gender:</b> $gender<br>\n";
         close $p;
         $flag = 1;
      }
   }
	return;
}

sub find_matches {
   my $word = $ENV{'QUERY_STRING'};
   @vars = split ('=', $word);
   $word = $vars[1];
   $word =~ s/\</&lt/;
   $word =~ s/\>/&gt/; 
   $name = $username;
   my $preferences = "./students/$name/preferences.txt";
   open my $p, "$preferences" or die "can not open $preferences: $!";
   @file = <$p>;
   $x = 0;
   while ($x <= $#file){
      if ($file[$x] =~ /^gender:/){
         $x++;
         chomp ($file[$x]);
         $file[$x] =~ s/\s//g;
         $genderpref = $file[$x];
      }
      if ($file[$x] =~ /^age:/){
         $x++;
         if ($file[$x] =~ /\s+min:/){
            $x++;
            chomp $file[$x];
            $file[$x] =~ s/\s//g;
            $minAgePref = $file[$x];
         }
         if ($file[$x+1] =~ /\s+max:/){
            $x+=2;
            chomp $file[$x];
            $file[$x] =~ s/\s//g;
            $maxAgePref = $file[$x];
         }
         if ($file[$x] =~ /\s+[1-9][0-9]+/){
            chomp $file[$x];
            $file[$x] =~ s/\s//g;
            $agePref = $file[$x];
         }
      }
      if ($file[$x] =~ /^height:/){
         $x++;
         if ($file[$x] =~ /^\s+min:/){
            $x++;
            $minHeight = $file[$x];
            $minHeight =~ s/\s//g;
            $minHeight =~ s/m//;
            chomp $minHeight;
         }
         if ($file[$x+1] =~ /^\s+max:/){
            $x+=2;
            $maxHeight = $file[$x];
            $maxHeight =~ s/\s//g;
            $maxHeight =~ s/m//;
            chomp $maxHeight;
         } 
      }
      if ($file[$x] =~ /^weight:/){
         $x++;
         if ($file[$x] =~ /^\s+min:/){
            $x++;
            $minHeight = $file[$x];
            $minHeight =~ s/\s//g;
            $minHeight =~ s/kg//;
            chomp $minWeight;
         }
         if ($file[$x+1] =~ /^\s+max:/){
            $x+=2;
            $maxHeight = $file[$x];
            $maxHeight =~ s/\s//g;
            $maxHeight =~ s/kg//;
            chomp $maxWeight;
         } 
      }
      $x++;
   }
   close $p;
	my @students = glob("$students_dir/*");
   print "<div class='col-md-3'>\n";
   print "<center>\n";
   $y = 0;
   $flag = 0;
   my @rejects = ();

   for $num (0..$#students) {
      my $student_to_show  = $students[$num];
      if ($flag == $y+1){
         print "</div>\n<div class='col-md-3'>\n<center>\n";
         $y++
      }
      
      my $profile_filename = "$student_to_show/profile.txt";
      my $profile_picture = "$student_to_show/profile.jpg";
      open $p, "$profile_filename" or die "can not open $profile_filename: $!";
      @file = <$p>;
      $x = 0;
      while ($x <= $#file){
         if ($file[$x] =~ /^birthdate:/){
            $x++;
            chomp ($file[$x]);
            $file[$x] =~ s/\s//g;
            @dob = split('/',$file[$x]);
            if ($dob[0] =~ /^[1-9][0-9]{3}$/){
               $age = 2014 - $dob[0];
            } elsif ($dob[1] =~ /^[1-9][0-9]{3}$/){
               $age = 2014 - $dob[1];
            } else {
               $age = 2014 - $dob[2];
            }
         }
         if ($file[$x] =~ /^username:/){
            $x++;
            chomp ($file[$x]);
            $file[$x] =~ s/\s//g;
            $username = $file[$x];
         }
         if ($file[$x] =~ /^gender:/){      
            $x++;
            chomp ($file[$x]);
            $file[$x] =~ s/\s//g;
            $gender = $file[$x];
         }
         if ($file[$x] =~ /^height:/){
            $x++;
            chomp $file[$x];
            $file[$x] =~ s/\s//g;
            $file[$x] =~ s/m//;
            $height = $file[$x];
         }
         if ($file[$x] =~ /^weight:/){
            $x++;
            chomp $file[$x];
            $file[$x] =~ s/\s//g;
            $file[$x] =~ s/kg//;
            $weight = $file[$x];
         }
         $x++;
      }
      if ($gender eq $genderpref && $name ne $username){
         if ($minAgePref && $maxAgePref){
            if ($minAgePref-5 < $age && $age < $maxAgePref+5){
               if ($minHeight && $maxHeight){
                  if ($minHeight-0.1 < $height && $height < $maxHeight+0.1){
                     if ($minWeight && $maxWeight){
                        if ($minWeight -5 < $weight && $weight < $maxWeight+5){
                           if (-e $profile_picture){
                              print "<a href='?user=$username'><img src = $profile_picture></a><br>\n";
                           } else {
                              print "<a href='?user=$username'>Profile picture not given<br></a>";
                           }  
                           print "<b>Username:</b> $username<br>\n";
                           print "<b>Age:</b> $age<br>\n";
                           print "<b>Gender:</b> $gender<br>\n";         
                           $flag++;
                        } else {
                           push @rejects, $profile_picture;
                           push @rejects ,$username;
                           push @rejects, $age;
                           push @rejects, $gender;
                        }                     
                     } else {
                        if (-e $profile_picture){
                           print "<a href='?user=$username'><img src = $profile_picture></a><br>\n";
                        } else {
                           print "<a href='?user=$username'>Profile picture not given<br></a>";
                        }
                        
                        print "<b>Username:</b> $username<br>\n";
                        print "<b>Age:</b> $age<br>\n";
                        print "<b>Gender:</b> $gender<br>\n";         
                        $flag++;
                     }
                  } else {
                     push @rejects, $profile_picture;
                     push @rejects ,$username;
                     push @rejects, $age;
                     push @rejects, $gender;
                  }
               } else {
                  if (-e $profile_picture){
                     print "<a href='?user=$username'><img src = $profile_picture></a><br>\n";
                  } else {
                     print "<a href='?user=$username'>Profile picture not given<br></a>";
                  }
                  
                  print "<b>Username:</b> $username<br>\n";
                  print "<b>Age:</b> $age<br>\n";
                  print "<b>Gender:</b> $gender<br>\n";         
                  $flag++;
               }
            }
         } else {
            if ($minHeight && $maxHeight){
               if ($minHeight-0.1 < $height && $height < $maxHeight+0.1){
                  if ($minWeight && $maxWeight){
                     if ($minWeight -5 < $weight && $weight < $maxWeight+5){
                        if (-e $profile_picture){
                           print "<a href='?user=$username'><img src = $profile_picture></a><br>\n";
                        } else {
                           print "<a href='?user=$username'>Profile picture not given<br></a>";
                        }  
                        print "<b>Username:</b> $username<br>\n";
                        print "<b>Age:</b> $age<br>\n";
                        print "<b>Gender:</b> $gender<br>\n";         
                        $flag++;
                     } else {
                        push @rejects, $profile_picture;
                        push @rejects ,$username;
                        push @rejects, $age;
                        push @rejects, $gender;
                     }                     
                  } else {
                     if (-e $profile_picture){
                        print "<a href='?user=$username'><img src = $profile_picture></a><br>\n";
                     } else {
                        print "<a href='?user=$username'>Profile picture not given<br></a>";
                     }
                     
                     print "<b>Username:</b> $username<br>\n";
                     print "<b>Age:</b> $age<br>\n";
                     print "<b>Gender:</b> $gender<br>\n";         
                     $flag++;
                  }
               } else {
                  push @rejects, $profile_picture;
                  push @rejects ,$username;
                  push @rejects, $age;
                  push @rejects, $gender;
               }
            }
         }         
      }
      close $p;      
   }
   while(scalar(@rejects) > 0){
      $profile_picture = shift @rejects;
      $username = shift @rejects;
      $age = shift @rejects;
      $gender = shift @rejects;
      if (-e $profile_picture){
         print "<a href='?user=$username'><img src = $profile_picture></a><br>\n";
      } else {
         print "<a href='?user=$username'>Profile picture not given<br></a>";
      }
      
      print "<b>Username:</b> $username<br>\n";
      print "<b>Age:</b> $age<br>\n";
      print "<b>Gender:</b> $gender<br>\n";         
      print "</div>\n<div class='col-md-3'>\n<center>\n";
   }
   
	return;
}

sub browse_users {
   my $n = $ENV{'QUERY_STRING'};
   if ($n =~ /n=[1-9][0-9]*/){
      @args = split (';', $n);
      @vars = split ('=', $args[1]);
      $n = $vars[1];
   } else {
      $n = 0;
   }
   $n++;
   print "
   <div class='container-fluid'>
            <div class='row'>
                <div class='col-md-2'>
    
   <div class='span2'>
   <a href='?page=Browse;n=$n' class='btn btn-primary btn-lg btn-block' role='button'>Next</a>
   ";
   $n--;
   if ($n > 0){
      $n=$n-1;
      print "<a href='?page=Browse;n=$n' class='btn btn-primary btn-lg btn-block' role='button'>Previous</a>";
      $n++;
   }
   print '</div></div>';
   
   $n = $n * 12;
   
	my @students = glob("$students_dir/*");
   print "<div class='col-md-3'>\n";
   print "<center>\n";
   for $num ($n..$n+11) {
      if ($num == $n + 4 || $num == $n + 8){
         print "</div>\n<div class='col-md-3'>\n<center>\n";
      }
      my $student_to_show  = $students[$num];
      my $profile_filename = "$student_to_show/profile.txt";
      my $profile_picture = "$student_to_show/profile.jpg";
      open my $p, "$profile_filename" or die "can not open $profile_filename: $!";
      @file = <$p>;
      $x = 0;
      while ($x <= $#file){
         if ($file[$x] =~ /^birthdate:/){
            $x++;
            chomp ($file[$x]);
            $file[$x] =~ s/\s//g;
            @dob = split('/',$file[$x]);            
            if ($dob[0] =~ /^[1-9][0-9]{3}$/){
               $age = 2014 - $dob[0];
            } elsif ($dob[1] =~ /^[1-9][0-9]{3}$/){
               $age = 2014 - $dob[1];
            } else {
               $age = 2014 - $dob[2];
            }
            
         }
         if ($file[$x] =~ /^username:/){
            $x++;
            chomp ($file[$x]);
            $file[$x] =~ s/\s//g;
            $username = $file[$x];
         }
         if ($file[$x] =~ /^gender:/){      
            $x++;
            chomp ($file[$x]);
            $file[$x] =~ s/\s//g;
            $gender = $file[$x];
         }
         $x++;
      }
      if (-e $profile_picture){
         print "<a href='?user=$username'><img src = $profile_picture></a><br>\n";
      } else {
         print "<a href='?user=$username'>Profile picture not given</a><br>\n";
      }
      print "<b>Username:</b> $username<br>\n";
      print "<b>Age:</b> $age<br>\n";
      print "<b>Gender:</b> $gender<br>\n";
      close $p;
   }
	return;
}

sub view_details {
   @array = split('=', $ENV{'QUERY_STRING'});
   my $student_to_show  = "$students_dir/$array[1]";
	my $profile_filename = "$student_to_show/profile.txt";
   my $profile_picture = "$student_to_show/profile.jpg";
	open my $p, "$profile_filename" or die "can not open $profile_filename: $!";
   open my $q, "$student_to_show/preferences.txt" or die "can not open $profile_filename: $!";
	@file = <$p>;
   @pref = <$q>;
   print "<pre>\n";
   if (-e $profile_picture){
      print "<img src = $profile_picture><br>\n";
   } else {
      print "<p>Profile picture not given<br></p>";
   }
   $x = 0;
   while ($x <= $#file){
      if ($file[$x] =~ /^password:/){
         $x++;
         while ($file[$x] =~ /^\s+/){
            $x++;
         }
      }
      if ($file[$x] =~ /^name:/){
         $x++;
         while ($file[$x] =~ /^\s+/){
            $x++;
         }
      }
      if ($file[$x] =~ /^email:/){
         $x++;
         while ($file[$x] =~ /^\s+/){
            $x++;
         }
      }
      if ($file[$x] =~ /^courses:/){
         $x++;
         while ($file[$x] =~ /^\s+/){
            $x++;
         }
      }
      if ($file[$x] =~ /^[A-Za-z]/){
         chomp ($file[$x]);
         print "<b><u>$file[$x]</u></b>\n";
      } else {
         chomp ($file[$x]);
         print "$file[$x]\n";
      }
      $x++;
   }
   print "</pre>";
	close $p;
   print "<p>Preferences</p>";
   print "<pre>";
   foreach $thing (@pref){
      if ($thing =~ /^[A-Za-z]/){
         chomp ($thing);
         print "<b><u>$thing</u></b>\n";
      } else {
         chomp ($thing);
         print "$thing\n";
      }
   }
   print "</pre>";
   close $q;
	return;
}

sub about_us {
   #print "<h1><center><b>About Us</b></center></h1>\n";
   #print menu();
   print "<font face ='garamond', size = '4', color='black'><p><center> This is an assignment that was handed out by Andrew Taylor as part of COMP2041.<br>
              Dating in real life is a really common thing, and finding \"the one\" is something that a lot of people strive for.<br>
              Our goal is to create a usable dating website where you will be able to search for and find other people to date.<br> 
              We aim to be able to match you up with the person of your dreams and hopefully help you with your love life!<br> 
              For a full outline of the spec, visit:\n";
   print "<a href='http://www.cse.unsw.edu.au/~cs2041/14s2/assignments/LOVE2041/'>http://www.cse.unsw.edu.au/~cs2041/14s2/assignments/LOVE2041/</a><br>\n";
   print "This website has been created by David Chacon of UNSW &#169 2014</center></p>\n";
   return;
}

#
# HTML placed at bottom of every screen
#
sub page_header {
	if (defined $cookie){
      print header(-cookie=>"x=$cookie");
   } else {
      print header;
   }
   print start_html("-title"=>"LOVE2041"),"\n";
   print center(h2(i("LOVE2041"))),"\n";
   return;
}

#this module is never used, merely used for reference once css implemented
sub menu {
   print '<a href="?page=Home"><input type="button" value="Home"></a>',"&nbsp\n"; 
   print '<a href="?page=Browse"><input type="button" value="Browse"></a>',"&nbsp\n";
   print '<a href="?page=About"><input type="button" value="About"></a>',"&nbsp\n";
   print textfield ('Search','Search for users'),"\n";
   return;
}

#
# HTML placed at bottom of every screen
# It includes all supplied parameter values as a HTML comment
# if global variable $debug is set
#
sub page_trailer {
   my $html = "";
	$html .= join("", map("<!-- $_=".param($_)." -->\n", param())) if $debug;
	$html .= end_html;
	return $html;
}

#credit to css bootstrap for all the design in this sub
sub navbar {
print '<nav class="navbar navbar-default" role="navigation">
        <div class="container-fluid">
          <!-- Brand and toggle get grouped for better mobile display -->
          <div class="navbar-header">
            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">
              <span class="sr-only">Toggle navigation</span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
            </button>
      ';
      
print '
          </div>

          <!-- Collect the nav links, forms, and other content for toggling -->
          <font color="blue">
          <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
            <ul class="nav navbar-nav">
      ';
      if ($ENV{'QUERY_STRING'} =~ /page=Home/){
     print '<li class="active"><a href="?page=Home">Home</a>
            <li><a href="?page=Browse">Browse</a></li>
              <li><a href="?page=About">About Us</a></li>';     
      } elsif ($ENV{'QUERY_STRING'} =~ /page=Browse/ || $ENV{'QUERY_STRING'} =~ /user=/){
     print '<li><a href="?page=Home">Home</a>
            <li class="active"><a href="?page=Browse">Browse</a></li>
              <li><a href="?page=About">About Us</a></li>';
      
      } elsif ($ENV{'QUERY_STRING'} =~ /page=About/){
     print '<li><a href="?page=Home">Home</a>
            <li><a href="?page=Browse">Browse</a></li>
              <li class="active"><a href="?page=About">About Us</a></li>';
      
      } else {
     print '<li><a href="?page=Home">Home</a>
            <li><a href="?page=Browse">Browse</a></li>
              <li><a href="?page=About">About Us</a></li>';
      
      }
print '  </ul>
            <form class="navbar-form navbar-left" role="search">
              <div class="form-group">
                <input type="text" class="form-control" name="searchQuery" placeholder="Search">
              </div>
              <button type="submit" class="btn btn-default">Submit</button>
            </form>
      ';
      if (defined $cookie && $cookie->value ne ''){
         $username = $cookie->name;
         print "
         <ul class='nav navbar-nav navbar-right'>
              <li><a href='?page=ViewProfile'>View Profile</a></li>
              <li><a href='?page=ViewMatches'>View Matches</a></li>
              <li><a href='?page=Home0'>Log Out : $username</a></li>
            </ul>
          </div><!-- /.navbar-collapse -->
        </div><!-- /.container-fluid -->
      </nav>","\n";
      
      } else {
         print '
            <ul class="nav navbar-nav navbar-right">
              <li><a href="?page=SignUp">Sign up</a></li>
              <li><a href="?page=LogIn">Log In</a></li>
            </ul>
          </div><!-- /.navbar-collapse -->
        </div><!-- /.container-fluid -->
      </nav>',"\n";         
      }
return;
}
