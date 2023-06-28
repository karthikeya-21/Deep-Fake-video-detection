<?php
    if (isset($_POST["submit"])) {
        // Specify the target directory to save the uploaded video
        $targetFile =basename($_FILES["videoFile"]["name"]);
        // Move the uploaded file to the target directory
        if (move_uploaded_file($_FILES["videoFile"]["tmp_name"], $targetFile)) {
            $fname=$_FILES["videoFile"]["name"];
            $ans = trim(shell_exec("python prediction.py $fname"));
        } else {
            echo "Sorry, there was an error uploading your file.";
        }
    }
?>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Deep Fake Video Detection</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
  <style>
    body {
      background-color: #f8f9fa;
    }
    
    .container2 {
      max-width: 500px;
      margin: 100px auto;
      padding: 30px;
      background-color: #fff;
      border-radius: 10px;
      box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    }
    
    .form-title {
      text-align: center;
      font-size: 24px;
      font-weight: bold;
      margin-bottom: 30px;
    }
    
    .navbar-brand {
      display: flex;
      font-size: 28px;
      font-weight: bold;
      justify-content: center;
      width: 100%;
    }

    .btn-primary {
      width: 100%;
    }

    .header {
      text-align: center;
      font-size: 28px;
      font-weight: bold;
      margin-bottom: 20px;
    }
    
    .content {
      text-align: justify;
      font-size: 18px;
      line-height: 1.6;
      margin-bottom: 40px;
    }

    .result {
      margin-top: 30px;
      text-align: center;
      font-size: 20px;
      font-weight: bold;
    }

    .video-preview {
      margin-top: 20px;
      text-align: center;
    }

    .video-preview video {
      max-width: 100%;
    }

    .container3{
      margin:0 120px;
    }

  </style>
</head>
<body>
<nav class="navbar navbar-dark bg-dark">
<div class="container">
<span class="navbar-brand text-center">Deep Fake Video Detection</span>
  </div>
</nav>
  <div class="container2">
    <h2 class="form-title">Deep Fake Video Detection</h2>
    <form action="" method="post" enctype="multipart/form-data">
      <div class="mb-3">
        <label for="videoFile" class="form-label">Upload Video</label>
        <input type="file" class="form-control" id="videoFile" name="videoFile" accept="video/*" oninput="previewVideo()" required>
      </div>
      <button type="submit" name="submit" class="btn btn-primary">Detect</button>
    </form>
    <div class="video-preview" id="videoPreview"></div>
  </div>

<?php if(isset($ans)): ?>
<div class="container3">
  

  <?php 
  if(strtolower($ans) === "fake"){ ?>
<h1 style="color:red;">The Input Video is : <?=$ans?></h1>
  <div class="content">
  <p><b>You can report it to the appropriate authorities or platforms. Here are some steps you can take to report a fake video:</b></p>

<p>1.Online platforms: If the fake video is hosted on a social media platform, video-sharing website, or any online platform, check their
   reporting or flagging options. Look for a "Report" or "Flag" button/link associated with the video and follow the provided instructions
    to report it as fake or manipulated content. Each platform may have its own reporting mechanisms.</p>

<p>2.Law enforcement agencies: If the fake video involves illegal activities, harassment, or poses a significant threat, consider reporting it
   to your local law enforcement agency. Provide them with any relevant information or evidence you have, such as the video file, links, or timestamps.</p>

<p>3.Cybercrime reporting centers: Many countries have specific cybercrime reporting centers or hotlines where you can report instances of online fraud,
   manipulation, or cyber-related offenses. Check with your local authorities or search for dedicated cybercrime reporting channels in your region.</p>

<p>4.Trusted news organizations: If the fake video has the potential to cause harm or is part of a disinformation campaign, you can reach out to trusted news
   organizations and share the video with them. News outlets may have investigative journalists or fact-checking teams who can further analyze the video and 
   raise awareness about its falsity.</p>

<p>Remember to provide as much information as possible when reporting a fake video, including the video file, links, timestamps, and any additional context or 
  evidence you have. Reporting fake videos helps in combating the spread of misinformation, protecting individuals from harm, and promoting online safety.</p>
  </div>
    <?php }else{ ?>
      <h1 style="color:green;">The Input Video is : <?=$ans?></h1>
    <?php } ?>
</div>
    
<?php endif; ?>

<div class="container3">
  <div class="header">What are Deep Fakes?</div>
      <div class="content">
      <p>Deepfake videos are manipulated or synthetic videos that use artificial intelligence (AI) and deep learning techniques to
         superimpose or replace the face of one person with the face of another person. The term "deepfake" is a combination of "deep learning" and "fake."
          Deep learning algorithms are used to analyze and generate realistic facial expressions and movements, allowing for the creation of videos that appear authentic and convincing.</p>

<p>Deepfake technology has gained attention due to its potential for misuse and the spread of misinformation. It has raised concerns about
   the ability to create realistic fake videos that can be used for various malicious purposes, such as spreading false information, manipulating
    public figures' images, or creating non-consensual explicit content.</p>
    <center><img src="fake.jpg" height="300" width="500" alt="fake"></center>
<p>However, deepfake technology is not inherently negative and has some legitimate applications as well. It can be used in the entertainment industry
   for special effects and digital character creation. Additionally, researchers and experts are actively working on developing deepfake detection techniques
    to identify and mitigate the risks associated with these manipulated videos.</p>

<p>It is important to be aware of the existence of deepfake videos and exercise critical thinking when consuming media content to distinguish between real and 
  manipulated videos.</p>
      </div>
</div>
  <script>
      function previewVideo() {
        var fileInput = document.getElementById("videoFile");
        var file = fileInput.files[0];
        
        if (file) {
          var video = document.createElement("video");
          video.src = URL.createObjectURL(file);
          video.controls = true;
          video.style.maxWidth = "100%";
          
          var videoPreview = document.getElementById("videoPreview");
          videoPreview.innerHTML = "";
          videoPreview.appendChild(video);
        }
      }
    </script>
</body>
</html>