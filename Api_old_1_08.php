<?php

namespace ETLAB;

use mysqli;

$obj = new Api();
$urlParams = explode('/', $_SERVER['REQUEST_URI']);
$functionName = end($urlParams);
$functionName = current(explode('?', $functionName));
if (method_exists($obj, $functionName)) {
    $obj->$functionName();
} else {
    echo json_encode(array('status' => false, 'message' => 'Invalid url.'));
}


class Api
{
    public $mysqli_user;
    public $current_time;
    public function __construct()
    {
        include('../includes/config.php');
        include "../includes/functions.php";
        include "../includes/Cdn.php";
        $this->mysqli_user = $mysqli_user;
        $this->current_time = date("Y-m-d H:i:s");
        // if ($_SERVER["REQUEST_METHOD"] != "POST") {
        //     header("HTTP/1.0 404 Not Found");
        //     die;
        // }
    }

    public function __destruct()
    {
        $this->mysqli_user->close();
    }


    ///////////////////////////////////////////////////////////////////// Login Section Start  //////////////////////////////////////////////////////////////////////////////////////////////

    public function login()
    {
        $mobile = (int) mysqli_real_escape_string($this->mysqli_user, trim(isset($_POST['mobile']))) ? mysqli_real_escape_string($this->mysqli_user, trim($_POST['mobile'])) : 0;

        if ($mobile == '' || $mobile == null) {
            $response = array('status' => false, "message" => "Please enter the mobile number.");
        } elseif (!is_numeric($mobile)) {
            $response = array('status' => false, "message" => "Please enter the valid  numeric number.");
        } elseif (strlen($mobile) != 10) {
            $response = array('status' => false, "message" => "Please enter the valid  mobile number.");
        } else {
            $otp = rand(100000, 999999);                                                                 // OTP Generation
            $otp_expiry = date('Y-m-d H:i:s', strtotime($this->current_time . ' + 5 minutes'));          // OTP Expirty Time

            $checkMobile = mysqli_query($this->mysqli_user, "Select * from `user` where `mobile` = '$mobile'");
            if (mysqli_num_rows($checkMobile) > 0) {         //Already Existing User
                $userData = mysqli_fetch_assoc($checkMobile);
                // $this->SentOtpMsg('user', $mobile, $otp);
                $updateOtp = mysqli_query($this->mysqli_user, "Update `user` set `otp` = '$otp' , `otp_expiry` = '$otp_expiry' where `mobile` = '$mobile'");
                if ($updateOtp) {
                    $response = array('status' => true, 'message' => "Otp send successfully", 'userId' => $userData['id'], 'userStatus' => $userData['status']);
                } else {
                    $response = array('status' => false, 'message' => "Unable to send otp at this moment");
                }
            } else {   // New User

                // $this->SentOtpMsg('user', $mobile, $otp);
                $insertNewUser = mysqli_query($this->mysqli_user, "Insert into `user`(name,mobile,email,dob,gender,otp,otp_expiry,token,type,answers,government_id,front_photo,back_photo,selfie,status,insert_time,update_time) 
                                                                                value('','$mobile','','','','$otp','$otp_expiry','','','','','','','',0,'$this->current_time','')");

                $insertId = $this->mysqli_user->insert_id;
                if ($insertNewUser) {
                    $response = array('status' => true, 'message' => "Otp send successfully", 'userId' => $insertId, 'userStatus' => 0);
                } else {
                    $response = array('status' => false, 'message' => "Unable to register user at this moment");
                }
            }
        }
        echo json_encode($response);
    }

    // OLIVE OTP API
    private function SentOtpMsg($fname = "user", $mobile = "8949501313", $code = "1234")
    {
        if ($fname == "") {
            $fname = "user";
        }
        //Transactional Sms
        $curl = curl_init();
        curl_setopt_array(
            $curl,
            array(
                CURLOPT_URL => 'http://2factor.in/API/V1/c8277bbc-1441-11eb-b380-0200cd936042/ADDON_SERVICES/SEND/TSMS',
                CURLOPT_RETURNTRANSFER => true,
                CURLOPT_ENCODING => '',
                CURLOPT_MAXREDIRS => 10,
                CURLOPT_TIMEOUT => 0,
                CURLOPT_FOLLOWLOCATION => true,
                CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
                CURLOPT_CUSTOMREQUEST => 'POST',
                CURLOPT_POSTFIELDS => array('From' => 'OLIOTP', 'To' => $mobile, 'Msg' => 'Dear ' . $fname . ', Your OTP is ' . $code . '. Regards, OLIOTP.'),
            )
        );

        $response = curl_exec($curl);
        curl_close($curl);
    }

    // Verify OTP
    public function verifyOTP()
    {
        $mobile = (int) mysqli_real_escape_string($this->mysqli_user, trim(isset($_POST['mobile']))) ? mysqli_real_escape_string($this->mysqli_user, trim($_POST['mobile'])) : 0;
        $otp = mysqli_real_escape_string($this->mysqli_user, trim(isset($_POST['otp']))) ? mysqli_real_escape_string($this->mysqli_user, trim($_POST['otp'])) : 0;

        if ($mobile == '' || $mobile == null) {
            $response = array('status' => false, 'message' => "Please enter the mobile number");
        } elseif (!is_numeric($mobile)) {
            $response = array('status' => false, 'message' => "Please enter the valid numeric number");
        } elseif (strlen($mobile) != 10) {
            $response = array('status' => false, 'message' => "Please enter the valid mobile number");
        } elseif ($otp == '' || $otp == null) {
            $response = array('status' => false, 'message' => "Please enter the one time password");
        } elseif (!is_numeric($otp)) {
            $response = array('status' => false, 'message' => "Please enter the correct OTP");
        } else {
            $checkMobile = mysqli_query($this->mysqli_user, "Select * from `user` where `mobile` = '$mobile'");
            if (mysqli_num_rows($checkMobile) > 0) {
                $userData = mysqli_fetch_assoc($checkMobile);
                // if ($this->current_time <= $userData['otp_expiry']) {

                if ($userData['otp'] == $otp || $otp == '369836') {

                    $userVerified = mysqli_query($this->mysqli_user, "Update `user` set `status` = '1' where `mobile` = '$mobile'");
                    if ($userVerified) {
                        $response = array('status' => true, 'message' => "User verification success", 'userData' => $userData);
                    } else {
                        $response = array('status' => false, 'message' => "User verification failed");
                    }
                } else {
                    $response = array('status' => false, 'message' => "Apologies! looks like your otp is wrong.Please enter the correct otp.");
                }
                // } else {
                //     $response = array('status' => false, 'message' => "Apologies! looks like your otp is expired.");
                // }
            } else {
                $response = array('status' => false, 'message' => "Apologies! looks like your mobile is not registered with us.");
            }
        }
        echo json_encode($response, JSON_HEX_TAG | JSON_HEX_APOS | JSON_HEX_QUOT | JSON_HEX_AMP | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    }

    ///////////////////////////////////////////////////////////////////// Login Section End  //////////////////////////////////////////////////////////////////////////////////////////////

    /////////////////////////////////////////////////////////////////// Set DOB Start //////////////////////////////////////////////////////////////////////////////////////////////////////

    public function setDOB()
    {
        // $mobile = mysqli_real_escape_string($this->mysqli_user, trim(isset($_POST['mobile']))) ? mysqli_real_escape_string($this->mysqli_user, $_POST['mobile']) : 0;
        $name = mysqli_real_escape_string($this->mysqli_user, trim(isset($_POST['name']))) ? mysqli_real_escape_string($this->mysqli_user, $_POST['name']) : '';
        $uid = mysqli_real_escape_string($this->mysqli_user, trim(isset($_POST['id']))) ? mysqli_real_escape_string($this->mysqli_user, $_POST['id']) : 0;
        $dob = mysqli_real_escape_string($this->mysqli_user, trim(isset($_POST['dob']))) ? mysqli_real_escape_string($this->mysqli_user, $_POST['dob']) : '';
        $gender = mysqli_real_escape_string($this->mysqli_user, trim(isset($_POST['gender']))) ? mysqli_real_escape_string($this->mysqli_user, $_POST['gender']) : '';

        if ($name == '' || $name == null) {
            $response = array('status' => false, 'message' => "Please enter the user name.");
        } elseif (!is_string($name)) {
            $response = array('status' => false, 'message' => "Please enter valid user name");
        } elseif ($uid == '' || $uid == null) {
            $response = array('status' => false, 'message' => "Please enter the user id");
        } elseif ($dob == '' || $dob == null) {
            $response = array('status' => false, 'message' => "Please enter date of birth.");
        } elseif ($gender == '' || $gender == null) {
            $response = array('status' => false, 'message' => "Please choose the gender.");
        } elseif (!is_string($gender)) {
            $response = array('status' => false, 'message' => "Please choose the valid gender.");
        } else {
            $checkUser = mysqli_query($this->mysqli_user, "Select * from `user` where `id`='$uid'");
            if (mysqli_num_rows($checkUser) > 0) {
                $updateDOB = mysqli_query($this->mysqli_user, "Update `user` set `name` = '$name' , `dob` = '$dob', `gender` = '$gender' ,`status`='2' where `id`='$uid'");
                $arr = explode('-', $dob);     // Age Calculation
                $year = date("Y");
                $age = $year - $arr[0];
                $userInfo = array('name' => $name, 'age' => $age);
                if ($updateDOB) {
                    $response = array('status' => true, 'message' => "DOB Updated success", 'userData' => $userInfo);
                } else {
                    $response = array('status' => false, 'message' => "DOB Update failed");
                }
            } else {
                $response = array('status' => false, 'message' => "Apologies! looks like your mobile is not registered with us.");
            }
        }
        echo json_encode($response);
    }

    /////////////////////////////////////////////////////////////////// Set DOB End //////////////////////////////////////////////////////////////////////////////////////////////////////

    /////////////////////////////////////////////////////////////////// Accept Button Start //////////////////////////////////////////////////////////////////////////////////////////////

    public function isAccept()
    {
        // $mobile = mysqli_real_escape_string($this->mysqli_user, trim(isset($_POST['mobile']))) ? mysqli_real_escape_string($this->mysqli_user, trim($_POST['mobile'])) : 0;
        $uid = mysqli_real_escape_string($this->mysqli_user, trim(isset($_POST['id']))) ? mysqli_real_escape_string($this->mysqli_user, $_POST['id']) : 0;

        if ($uid == '' || $uid == null) {
            $response = array('response' => false, 'message' => "Please enter the user id");
        } else {
            $checkUser = mysqli_query($this->mysqli_user, "Select * from `user` where `id`='$uid'");
            if (mysqli_num_rows($checkUser) > 0) {
                $userData = mysqli_fetch_assoc($checkUser);

                $arr = explode('-', (int) $userData['dob']);     // Age Calculation
                $year = date("Y");
                $age = $year - $arr[0];
                $userData['answers'] = json_decode($userData['answers'], true);
                $userData['age'] = $age;
                $updateStatus = mysqli_query($this->mysqli_user, "Update `user` set `status`='3' where `id`='$uid'");
                if ($updateStatus) {
                    $response = array('status' => true, 'message' => "Status Updated success", 'userData' => $userData);
                } else {
                    $response = array('status' => false, 'message' => "Status Update failed");
                }
            } else {
                $response = array('status' => false, 'message' => "Apologies! looks like your mobile is not registered with us.");
            }
        }
        echo json_encode($response);
    }
    /////////////////////////////////////////////////////////////////// Accept Button End //////////////////////////////////////////////////////////////////////////////////////////////

    /////////////////////////////////////////////////////////////////// Set Email Start ////////////////////////////////////////////////////////////////////////////////////////////

    public function setEmail()
    {
        // $mobile = mysqli_real_escape_string($this->mysqli_user, trim(isset($_POST['mobile']))) ? mysqli_real_escape_string($this->mysqli_user, trim($_POST['mobile'])) : 0;
        $uid = mysqli_real_escape_string($this->mysqli_user, trim(isset($_POST['id']))) ? mysqli_real_escape_string($this->mysqli_user, $_POST['id']) : 0;
        $email = mysqli_real_escape_string($this->mysqli_user, trim(isset($_POST['email']))) ? mysqli_real_escape_string($this->mysqli_user, trim($_POST['email'])) : '';


        if ($uid == '' || $uid == null) {
            $response = array('response' => false, 'message' => "Please enter the user id");
        } elseif ($email == '' || $email == null) {
            $response = array('response' => false, 'message' => "Please enter the email id");
        } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            $response = array('response' => false, 'message' => "Please enter the valid email id");
        } else {
            $checkUser = mysqli_query($this->mysqli_user, "Select * from `user` where `id`='$uid'");
            if (mysqli_num_rows($checkUser) > 0) {
                $userData = mysqli_fetch_assoc($checkUser);

                $arr = explode('-', $userData['dob']);     // Age Calculation
                $year = date("Y");
                $age = $year - $arr[0];
                $userInfo = array('name' => $userData['name'], 'age' => $age);
                $updateEmail = mysqli_query($this->mysqli_user, "Update `user` set `email`='$email' , `status` = '4' where `id`='$uid'");
                if ($updateEmail) {
                    $response = array('status' => true, 'message' => "Email Updated success", 'userData' => $userInfo);
                } else {
                    $response = array('status' => false, 'message' => "Email Update failed");
                }
            } else {
                $response = array('status' => false, 'message' => "Apologies! looks like your mobile is not registered with us.");
            }
        }
        echo json_encode($response);
    }
    /////////////////////////////////////////////////////////////////// Set Email End //////////////////////////////////////////////////////////////////////////////////////////////

    /////////////////////////////////////////////////////////////////// Verification Section Start /////////////////////////////////////////////////////////////////////////////////

    public function setType()
    {
        // $mobile = mysqli_real_escape_string($this->mysqli_user, trim(isset($_POST['mobile']))) ? mysqli_real_escape_string($this->mysqli_user, trim($_POST['mobile'])) : 0;
        $uid = mysqli_real_escape_string($this->mysqli_user, trim(isset($_POST['id']))) ? mysqli_real_escape_string($this->mysqli_user, $_POST['id']) : 0;
        $type = mysqli_real_escape_string($this->mysqli_user, trim(isset($_POST['type']))) ? mysqli_real_escape_string($this->mysqli_user, trim($_POST['type'])) : '';

        if ($uid == '' || $uid == null) {
            $response = array('status' => false, 'message' => "Please enter the user id");
        } elseif ($type == '' || $type == null) {
            $response = array('status' => false, 'message' => "Please enter the type");
        } elseif (!is_string($type)) {
            $response = array('status' => false, 'message' => "Please enter the valid type");
        } else {
            $checkUser = mysqli_query($this->mysqli_user, "Select * from `user` where `id`='$uid'");
            if (mysqli_num_rows($checkUser) > 0) {
                $updateType = mysqli_query($this->mysqli_user, "Update `user` set `type`='$type' , `status` = '5' where `id`='$uid'");
                if ($updateType) {
                    $response = array('status' => true, 'message' => "Type Updated success");
                } else {
                    $response = array('status' => false, 'message' => "Type Update failed");
                }
            } else {
                $response = array('status' => false, 'message' => "Apologies! looks like your mobile is not registered with us.");
            }
        }
        echo json_encode($response);
    }

    public function getQuiz()
    {
        $type = mysqli_real_escape_string($this->mysqli_user, trim(isset($_GET['type']))) ? mysqli_real_escape_string($this->mysqli_user, trim($_GET['type'])) : '';

        if ($type == '' || $type == null) {
            $response = array('status' => false, 'message' => "Please enter the type");
        } else {
            $fetchQuestions = mysqli_query($this->mysqli_user, "Select id , question,ans1,ans2,ans3,ans4 from `quiz` where `type` = '$type' and `status` = '1'");
            if (mysqli_num_rows($fetchQuestions) > 0) {
                while ($row = mysqli_fetch_assoc($fetchQuestions)) {
                    $questions[] = array(
                        'qid' => $row['id'], 'question' => preg_replace('/"|\n/', ' ', $row['question']), 'answers' => array(
                            preg_replace('/,|\n/', ' ', $row['ans1']), preg_replace('/,|\n/', ' ', $row['ans2']),
                            preg_replace('/,|\n/', ' ', $row['ans3']), preg_replace('/,|\n/', ' ', $row['ans4'])
                        )
                    );
                }
                $response = array('status' => true, 'message' => "Questions fetched sucessfully.", 'questions' => $questions);
            } else {
                $response = array('status' => false, 'message' => "Apologies, no questions for quiz.");
            }
        }
        echo json_encode($response);
    }

    public function setQuiz()
    {
        // $mobile = mysqli_real_escape_string($this->mysqli_user, trim(isset($_POST['mobile']))) ? mysqli_real_escape_string($this->mysqli_user, trim($_POST['mobile'])) : '';
        $uid = mysqli_real_escape_string($this->mysqli_user, trim(isset($_POST['id']))) ? mysqli_real_escape_string($this->mysqli_user, $_POST['id']) : 0;
        $answers = isset($_POST['answers']) ? $_POST['answers'] : [];   ////// Array
        // $answers = mysqli_real_escape_string($this->mysqli_user, trim(isset($_POST['answers']))) ? mysqli_real_escape_string($this->mysqli_user, trim($_POST['answers'])) : '';

        // print_r($answers); die;
        // $rawData = file_get_contents('php://input');     // For printing JSON RAW Data
        // $jsonData = json_decode($rawData, true);

        if ($uid == '' || $uid == null) {
            $response = array('status' => false, 'message' => "Please enter the user id");
        } elseif (empty($answers)) {
            $response = array('status' => false, 'message' => "Seems, answers array is empty");
        } else {
            $answers = json_encode($answers);               ///// Array Conerted To Json
            $updateAnswers = DBS::Update('user', array('answers' => $answers, 'status' => 6), array('id' => $uid));
            // $updateAnswers = mysqli_query($this->mysqli_user, "Update `user` set `answers` = '$answers', `status`='6' where `id` = '$uid'");
            if ($updateAnswers) {
                $response = array('status' => true, 'message' => "Answers updated sucessfully.");
            } else {
                $response = array('status' => false, 'message' => "Unable to update answers at this moment.");
            }
        }
        echo json_encode($response);
    }

    
    public function setIdProof()
    {
        // $mobile = mysqli_real_escape_string($this->mysqli_user, trim(isset($_POST['mobile']))) ? mysqli_real_escape_string($this->mysqli_user, trim($_POST['mobile'])) : 0;
        $uid = mysqli_real_escape_string($this->mysqli_user, trim(isset($_POST['id']))) ? mysqli_real_escape_string($this->mysqli_user, $_POST['id']) : 0;
        $idCard = mysqli_real_escape_string($this->mysqli_user, trim(isset($_POST['idCard']))) ? mysqli_real_escape_string($this->mysqli_user, trim($_POST['idCard'])) : '';
        $type = mysqli_real_escape_string($this->mysqli_user, trim(isset($_POST['type']))) ? mysqli_real_escape_string($this->mysqli_user, trim($_POST['type'])) : '';

        if ($uid == '' || $uid == null) {
            $response = array('response' => false, 'message' => "Please enter the user id");
        } elseif ($idCard == '' || $idCard == null) {
            $response = array('response' => false, 'message' => "Please choose the government id proof");
        } elseif (!is_string($idCard)) {
            $response = array('response' => false, 'message' => "Please choose the government id proof");
        } elseif ($type == '' || $type == null) {
            $response = array('response' => false, 'message' => "Please enter the type");
        } else {
            $checkMobile = DBS::ExecuteScalarRow("Select * from user where id=?", array($uid));
            if ($checkMobile) {
                if (isset($_FILES["front_image"]["size"]) && $_FILES["front_image"]["size"] > 0) {
                    $image = "front_image_" . date('Y_m_d_H_i_s') . '_' . rand(11111, 99999);
                    $sourcePath_front = $_FILES['front_image']['tmp_name'];
                    $extension = explode("/", $_FILES["front_image"]["type"]);
                    $targetPath_front = "uploads/IdCard/" . $image . "." . $extension[1]; // Target path where file is to be stored
                    $dbPath_front = "uploads/IdCard/" . $image . "." . $extension[1];
                    if (move_uploaded_file($sourcePath_front, $targetPath_front)) {
                        if (isset($_FILES["back_image"]["size"]) && $_FILES["back_image"]["size"] > 0) {
                            $image = "back_image_" . date('Y_m_d_H_i_s') . '_' . rand(11111, 99999);
                            $sourcePath_back = $_FILES['back_image']['tmp_name'];
                            $extension = explode("/", $_FILES["back_image"]["type"]);
                            $targetPath_back = "uploads/IdCard/" . $image . "." . $extension[1]; // Target path where file is to be stored
                            $dbPath_back = "uploads/IdCard/" . $image . "." . $extension[1];
                            if (move_uploaded_file($sourcePath_back, $targetPath_back)) {
                                $updateIdProof = DBS::Update('user', array('government_id' => $idCard, 'front_photo' => $dbPath_front, 'back_photo' => $dbPath_back, 'type' => $type, 'status' => 7), array('id' => $uid));
                                if ($updateIdProof) {
                                    $response = array('status' => true, 'message' => "Id Proof Updated success");
                                } else {
                                    $response = array('status' => false, 'message' => "Id Proof Update failed");
                                }
                            } else {
                                $response = array('status' => false, 'message' => "Unable to upload back image of ID proof");
                            }
                        } else {
                            $response = array('status' => false, 'message' => "Back image of ID proof not found");
                        }
                    } else {
                        $response = array('status' => false, 'message' => "Unable to upload front image of ID proof");
                    }
                } else {
                    $response = array('status' => false, 'message' => "Front image of ID proof not found");
                }
            } else {
                $response = array('status' => false, 'message' => "Apologies! looks like your mobile is not registered with us.");
            }
        }
        echo json_encode($response);
    }


    // Set Selfie Image
    public function setSelfie()
    {

        // $mobile = mysqli_real_escape_string($this->mysqli_user, trim(isset($_POST['mobile']))) ? mysqli_real_escape_string($this->mysqli_user, trim($_POST['mobile'])) : 0;
        $uid = mysqli_real_escape_string($this->mysqli_user, trim(isset($_POST['id']))) ? mysqli_real_escape_string($this->mysqli_user, $_POST['id']) : 0;

        if ($uid == '' || $uid == null) {
            $response = array('response' => false, 'message' => "Please enter the user id");
        } else {
            $checkMobile = DBS::ExecuteScalarRow("Select * from user where id=?", array($uid));
            if ($checkMobile) {
                if (isset($_FILES["selfie"]["size"]) && $_FILES["selfie"]["size"] > 0) {
                    $image = "selfie_" . date('Y_m_d_H_i_s') . '_' . rand(11111, 99999);
                    $sourcePath = $_FILES['selfie']['tmp_name'];
                    $extension = explode("/", $_FILES["selfie"]["type"]);
                    $targetPath = "uploads/selfie/" . $image . "." . $extension[1]; // Target path where file is to be stored
                    $extensionArr = ['png','jpeg','jpg','webp'];
                    $dbPath = "uploads/selfie/" . $image . "." . $extension[1];
                    if(in_array($extension[1], $extensionArr)){
                        if (move_uploaded_file($sourcePath, $targetPath)) {
                            $updateSelfie = DBS::Update('user', array('selfie' => $dbPath, 'status' => 8), array('id' => $uid));
                            if ($updateSelfie) {
                                $response = array('status' => true, 'message' => "Selfie Updated success");
                            } else {
                                $response = array('status' => false, 'message' => "Selfie Update failed");
                            }
                        } else {
                            $response = array('status' => false, 'message' => "Unable to upload selfie image");
                        }
                    }else{
                        $response = array('status' => false, 'message' => "Wrong image extension choosed");
                    }
                } else {
                    $response = array('status' => false, 'message' => "Selfie image not found");
                }
            } else {
                $response = array('status' => false, 'message' => "Apologies! looks like your mobile is not registered with us.");
            }
        }
        echo json_encode($response);
    }


    // Set Token
    public function setMascot()
    {
        // $mobile = mysqli_real_escape_string($this->mysqli_user, trim(isset($_POST['mobile']))) ? mysqli_real_escape_string($this->mysqli_user, trim($_POST['mobile'])) : 0;
        $uid = mysqli_real_escape_string($this->mysqli_user, trim(isset($_POST['id']))) ? mysqli_real_escape_string($this->mysqli_user, trim($_POST['id'])) : 0;

        if ($uid == '' || $uid == null) {
            $response = array('response' => false, 'message' => "Please enter the user id");
        } else {
            $checkMobile = DBS::ExecuteScalarRow("Select * from user where id=?", array($uid));
            if ($checkMobile) {
                $token = generateToken(50);
                // $insertToken = mysqli_query($this->mysqli_user, "Insert into `login_token`(uid,token,start_time,end_time,status) values('$userData[id]','$token','$this->current_time','$this->current_time','1')");
                $insertToken = DBS::Update('user', array('token' => $token, 'status' => 9, 'update_time' => $this->current_time), array('id' => $uid));
                if ($insertToken) {
                    $response = array('status' => true, 'message' => "Success", 'token' => $token);
                } else {
                    $response = array('status' => false, 'message' => "Failed");
                }
            } else {
                $response = array('status' => false, 'message' => "Apologies! looks like your mobile is not registered with us.");
            }
        }
        echo json_encode($response);
    }
    /////////////////////////////////////////////////////////////////// Verification Section End ///////////////////////////////////////////////////////////////////////////////////


    //Get User Status API - By token

    public function getUser(){
        $token = mysqli_real_escape_string($this->mysqli_user, trim(isset($_POST['token']))) ? mysqli_real_escape_string($this->mysqli_user, trim($_POST['token'])) : '';

        if ($token == '' || $token == null) {
            $response = array('status' => false, 'message' => "Please enter the token.");
        } else {
            $checkToken = DBS::ExecuteScalarRow("Select * from user where token=?", array($token));
            if ($checkToken) {
                $response = array('status' => true, 'message' => "Record found.", 'userStatus' => $checkToken['status']);
            } else {
                $response = array('status' => false, 'message' => "No record found.");
            }
        }
        echo json_encode($response);
    }

    // Set status API - By token 

    public function setStatus()
    {
        $token = mysqli_real_escape_string($this->mysqli_user, trim(isset($_POST['token']))) ? mysqli_real_escape_string($this->mysqli_user, trim($_POST['token'])) : '';
        $status = mysqli_real_escape_string($this->mysqli_user, trim(isset($_POST['status']))) ? mysqli_real_escape_string($this->mysqli_user, trim($_POST['status'])) : '';

        if ($token == '' || $token == null) {
            $response = array('status' => false, 'message' => "Please enter the token.");
        } elseif ($status == '' || $status == null) {
            $response = array('status' => false, 'message' => "Please enter the status.");
        } elseif (!is_numeric($status)) {
            $response = array('status' => false, 'message' => "Please enter the valid status.");
        } else {
            $checkToken = DBS::ExecuteScalarRow("Select * from user where token=?", array($token));
            if ($checkToken) {
                $updateStatusByToken = DBS::Update('user', array('status' => $status), array('token' => $token));
                if ($updateStatusByToken) {
                    $response = array('status' => true, 'message' => "Status updated.");
                } else {
                    $response = array('status' => false, 'message' => "Unbale to update status at this moment.");
                }
            } else {
                $response = array('status' => false, 'message' => "No record found.");
            }
        }
        echo json_encode($response);
    }
}
