<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Lisanic</title>
<link rel="stylesheet" type="text/css" href="css/style.css" />
<link rel="stylesheet" type="text/css" href="style_calender.css" />
<link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.css" />
<link rel="shortcut icon" href="favicon.ico" />
<!--[if lt IE 9]>
<script type="text/javascript" src="js/html5.js"></script>
<![endif]-->
</head>

<body>
<div id="outer_wrapper">
	<header id="header" class="headings">
    	<div class="wrapper">
    	<nav class="top_nav">
        	<ul>
            	<li><a href="index.php" class="homes">Home</a></li>
            	<li><a href="index.php">Individuals</a></li>
                <li><a href="schools.php">Schools</a></li>
                <li><a href="about.php">About</a></li>
                <li><a href="conact.php">Support</a></li>
            </ul>
            <div class="clear"></div>
        </nav>
        
        <div class="sec_nav">
        <div class="logo_left">
			<h1><a href="index.php"><img src="images/logo.png" height="" width="" alt="Lisanic" /></a></h1>        
        </div>
        <nav class="main_nav">
        	<div class="welcome_user">
            	<ul>
                	<li>John Doe</li>
                    <li>|</li>
                   <li><a href="index.php">Sign out</a></li>
                </ul>
            </div>
        </nav>
        <div class="clear"></div>
    	</div>
        <div class="nav_lines"></div>
        <div class="breadcums">
        	<div class="left">
            	<span class="homes"><a href="index.php"><img src="images/home_icons.png" height="" width="" alt="Home Lisanic" /></a></span> &gt;
                <a href="index.php">Lisanic</a> &gt; 
                <span>Lessonhub2</span>
            </div>
            <div class="right">
                <a href="dashboard.php">Dashboard</a>
                <a href="lesson-cycle.php">Lesson Hub</a>
                <a href="lesson-phrase.php">Lesson 1</a>
                <a href="lesson.php" class="active">Lesson 2 </a>
                <a href="lesson-hub3.php">Lesson 3</a>
                <a href="lesson4.php">Lesson 4</a>
            </div>
            <div class="clear"></div>
        </div>
        </div>
    </header>
<!--<script src="js/quantae-js-engine/Quantae.js"></script>
<script src="js/quantae-js-engine/sentence_4a.js"></script>
<script src="js/quantae-js-engine/QAPlotter.js"></script>-->

<section class="body_sections">
    <div class="wrapper">
    	<!--<div class="banner_outer">-->
    	<!--<div class="banner" style="overflow:visible;">
        	
        </div>-->
        <div class="pages_content_slide">
             <div class="slide">
        	 <img src="images/Test_slide_a.png" height="500px" width="890px" alt="Slide" />
             </div>
        	  <div class="mid_lesson_form_wrap1">
                <a class="left" href="#">Left</a>
                <a class="right" href="#">Right</a>
                <div class="video_lesson">
                
                <div id="mediaplayer">JW Player goes here</div>
				
                  	<script type="text/javascript" src="jwplayer/jwplayer.js"></script>
                    
	<?php
	//echo $_SERVER['HTTP_USER_AGENT'];
	 if(strstr($_SERVER['HTTP_USER_AGENT'],'iPhone') || strstr($_SERVER['HTTP_USER_AGENT'],'iPad')  || strstr($_SERVER['HTTP_USER_AGENT'],'Linux')) {?>
    	<script type="text/javascript">
						jwplayer("mediaplayer").setup({
						flashplayer: "jwplayer/player.swf",
						file: "video/003.2.mp4",
						image: "jwplayer/intro.gif",
						'controlbar': '',
						'id': 'playerID',
						'autostart': 'true',
						'backcolor': 'fff',
						'frontcolor': 'c64e96',
						'screencolor': 'fff',
						'lightcolor': 'ccc',
						'width': '327',
						'wmode': 'transparent',
    					'height': '420',
						'stretching': 'exactfit'
					});
					
	</script>
			<?php } else {?>
            
                	<script type="text/javascript">
						jwplayer("mediaplayer").setup({
						flashplayer: "jwplayer/player.swf",
						file: "../video/[[video_file]]",
						image: "jwplayer/intro2.gif",
						'controlbar': '',
						'width': '327',
    					'height': '420'
					});
					</script>
                    
				<?php }?>	
					
                
                 </div>
                
                
                	<!--
                    <div id="paperToDraw" class="base">
    						<h1 style="margin-top:90px;">How do you say in Arabic <br />"The man's house"?</h1>
                            	<div style="text-align:center; margin:50px 0;">
                                	<img src="images/arabic_language.jpg" />
                                </div>
    
					</div>
                    -->
						<script type="text/javascript">
    var paper = document.getElementById("paperToDraw");
	//alert(paper);
    Quantae.QAPlotter.PlotPage(paper, sentence, false);
    
    Quantae.QAPlotter.BalanceBlankSpace = function()
    {
        var blankDiv = document.getElementById(Quantae.QAPlotter.PlottedQuesFrags_Base + Quantae.QAPlotter.BlankIndex);
        var subAnswersDiv = document.getElementById(Quantae.QAPlotter.PlottedAnswers_SubParent_Base);
        
        var max = -1;
        //subAnswersDiv.childNodes[0].clientWidth;
        /*for (var i = 0; i < subAnswersDiv.childNodes.length; i++)
        {
            if (subAnswersDiv.childNodes[i].clientWidth > max)
                max = subAnswersDiv.childNodes[i].clientWidth;
        }*/
        
        alert(max);
        
       // subAnswersDiv.style.top = (blankDiv.clientHeight + Quantae.QAPlotter.BottomMargin_Answers) + 'px';
        
        //blankDiv.style.width = subAnswersDiv.clientWidth + 'px';
    }
    
    
    
  //  Quantae.QAPlotter.BalanceBlankSpace();
</script>

				<!--<div class="answer_english">The house of the man</div>-->

                </div>
            </div>
        <?php /*?><div class="bottom_bann_links">
         	<span class="left_r"></span><span class="right_r"></span>
         		<ul class="left" style="display:none;">
                	<li class="facebook"><a href="#">Facebook</a></li>
                    <li class="flag"><a href="#">Flag</a></li>
                    <li class="notification"><a href="#">Notification</a></li>
                </ul>
                
                <ul class="right" style="display:none;">
                	<li class="search"><a href="#">Search</a></li>
                    <li class="bookmarks"><a href="#">Bookmark</a></li>
                    <li class="locations"><a href="#">Location</a></li>
                </ul>
                <div class="clear"></div>
         </div><?php */?>
      <!--  </div>-->
    </div>
    </section>
<?php include_once('includes/footer.php');?>    
