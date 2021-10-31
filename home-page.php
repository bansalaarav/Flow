<!DOCTYPE html>
<html lang="en" dir="ltr">
    <head>
        <style>
        @font-face {
          font-family: "Product Sans Regular";
          src: url("./ProductSansRegular.ttf");
        }

        @font-face {
          font-family: "Product Sans Bold";
          src: url("./ProductSansBold.ttf");
        }

        body {
            margin: 0;
            padding: 0;
            background-color: #2788E4;
        }

        #image-container {
            margin-top: 5vh;
            margin-left: 50%;
            height: 45%;
            width: 45%;
            border-radius: 3.5vw;
        }

        #title {
            font-size: 5vh;
            font-family: 'Product Sans Bold', sans-serif;
            color: white;
            margin-left: 3vw;
            margin-top: -50vh;
        }

        #subtitle {
            font-size: 4vh;
            font-family: 'Product Sans Regular', sans-serif;
            color: white;
            margin-left: 3vw;
            margin-right: 53%;
        }

        #explore-button {
            margin-left: 2.5vw;
            margin-top: 4vh;
            margin-bottom: 4vh;
            display: block;
            width: 17vw;
            height: 7vh;
            color: white;
            font-size: 3vh;
            background-color: black;
            border-radius: 5vw;
            border: none;
            box-shadow: 0px 0px 10px 1px black;
            font-family: 'Product Sans Regular', sans-serif;
        }

        #explore-button-2 {
            margin-left: 2.5vw;
            margin-bottom: 15px;
            width: 17vw;
            height: 7vh;
            color: white;
            font-size: 3vh;
            background-color: black;
            border-radius: 5vw;
            border: none;
            box-shadow: 0px 0px 10px 1px black;
            font-family: 'Product Sans Regular', sans-serif;
        }

        #explore-button:hover {
            box-shadow: 0px 0px 5px 1px black;
            cursor: pointer;
        }

        #explore-button-2:hover {
            box-shadow: 0px 0px 5px 1px black;
            cursor: pointer;
        }

        .divider-class-one {
            height: 20vh;
        }

        @media (max-width: 1200px) {
            #image-container {
                margin-left: 10%;
                height: 450px;
                width: 80%;
                margin-bottom: 0;
            }

            #title {
                text-align: center;
                margin-top: 50px;
            }

            .divider-class-one {
                height: 0px;
            }

            #subtitle {
                text-align: center;
                margin-left: 10px;
                margin-right: 10px;
            }

            #explore-button {
                margin-left: 20px;
                width: 45%;
                display: inline-block;
            }

            #explore-button-2 {
                width: 45%;
                margin-left: 20px;
            }
        }
        </style>
        <meta charset="utf-8">
        <title>Welcome to FLOW</title>
    </head>
    <body>
        <?php include 'header.html'; ?>
        <img src="drone.gif" alt="flying-drone" id="image-container">
        <div id="title">Drones are the future...</div>
        <div id="subtitle">And our work at flow is to help you know what's going on in the drone world! Would you like to...</div>
        <button id="explore-button">Check the blog out</button>
        <button id="explore-button-2">or play a short quiz?</button>
        <div class="divider-class-one">

        </div>
        <?php include 'footer.html'; ?>
    </body>
</html>
