// https://stackoverflow.com/questions/11381673/detecting-a-mobile-browser
var isMobile = {
   Android: function() {
       return navigator.userAgent.match(/Android/i);
   },
   BlackBerry: function() {
       return navigator.userAgent.match(/BlackBerry/i);
   },
   iOS: function() {
       return navigator.userAgent.match(/iPhone|iPad|iPod/i);
   },
   Opera: function() {
       return navigator.userAgent.match(/Opera Mini/i);
   },
   Windows: function() {
       return navigator.userAgent.match(/IEMobile/i) || navigator.userAgent.match(/WPDesktop/i);
   },
   any: function() {
       return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
   }
};
var obj = {"local":[[52,51,52,53,53,53,53,53,53,52,51,52,55,56,58,59,60,59,57,55,55,54,54,53,53,53,53,53,54,54,55,55],[52,51,52,53,53,53,53,52,52,51,50,52,55,55,57,58,58,58,57,55,55,54,53,53,53,53,52,53,53,53,54,54],[54,53,55,56,56,56,55,55,54,53,53,56,58,58,59,60,60,61,60,58,59,58,58,57,57,56,55,56,56,56,56,56],[55,55,56,56,56,56,55,55,54,54,54,57,60,59,60,60,60,61,61,59,60,60,59,58,58,57,57,57,57,57,57,56],[55,55,57,57,56,56,56,56,55,56,57,60,61,60,61,61,60,61,61,60,61,61,61,60,60,58,58,58,58,57,57,56],[55,56,57,57,56,56,56,56,56,57,58,61,61,61,61,60,59,60,61,60,61,62,62,61,60,59,58,58,58,57,57,56],[55,56,57,56,55,56,57,57,58,60,61,62,63,62,62,61,60,60,60,60,61,62,62,62,62,61,60,60,59,57,57,56],[55,55,57,56,55,56,57,57,58,61,61,63,63,62,62,61,59,60,59,59,60,61,62,62,62,61,61,60,59,57,57,56],[55,56,57,56,55,56,58,59,59,61,61,62,63,63,62,61,59,60,59,59,60,61,62,61,62,62,61,61,60,58,58,56],[55,56,57,56,55,56,58,59,59,59,59,61,62,62,62,60,59,59,58,58,60,61,61,61,61,61,61,61,60,58,58,56],[56,56,58,57,56,57,59,59,59,59,59,60,61,61,61,60,58,59,59,59,60,61,61,60,61,61,61,61,60,59,60,57],[56,56,58,58,56,58,59,58,58,58,58,59,60,59,59,58,57,58,58,59,60,61,60,59,59,60,60,60,60,59,60,57],[56,56,58,58,57,58,60,59,59,59,58,59,60,59,59,58,57,58,59,59,60,61,60,59,59,59,59,60,60,60,60,58],[56,56,58,59,58,59,60,60,60,60,60,61,60,60,59,58,58,58,59,59,60,62,60,58,58,57,57,58,60,60,60,58],[56,56,58,59,58,59,60,60,61,61,61,61,61,60,60,59,59,59,58,58,60,61,60,58,57,57,56,58,59,59,60,58],[56,57,59,59,59,60,60,60,61,61,60,61,61,61,61,61,61,60,58,58,60,62,61,59,58,57,56,58,59,59,60,58],[57,57,59,59,59,60,60,59,59,59,59,60,61,62,62,62,61,61,58,57,59,62,62,60,59,57,56,57,58,59,60,58],[58,58,60,61,60,60,60,59,59,59,58,59,61,62,62,62,61,61,58,57,59,61,62,60,60,58,57,57,58,58,59,58],[58,58,61,61,60,60,60,59,58,57,56,57,60,61,62,61,60,59,57,56,58,60,61,60,60,58,57,57,57,57,58,57],[59,60,62,62,61,61,61,60,59,57,56,57,60,61,62,61,60,59,57,56,57,59,60,60,61,59,58,58,57,57,58,57],[59,60,63,63,61,62,61,60,59,56,55,56,58,59,60,60,59,58,56,56,56,57,59,60,61,60,58,58,57,56,57,56],[61,62,64,64,63,63,62,61,60,57,56,57,59,59,60,60,59,58,56,56,56,57,60,61,62,62,60,59,57,57,57,56],[60,62,64,64,63,63,63,62,61,58,57,57,58,59,59,59,58,57,56,55,55,56,60,61,62,62,61,60,57,57,57,56],[61,62,65,65,64,65,64,63,63,61,59,60,60,59,60,59,58,57,56,56,56,58,60,61,63,63,61,61,59,58,58,57],[60,61,64,65,64,65,64,64,63,61,60,61,60,59,59,58,57,57,56,56,56,58,61,61,63,62,61,60,59,58,58,57],[60,61,65,66,64,65,65,64,64,63,63,64,63,61,61,59,58,58,57,57,58,61,62,62,63,62,61,60,59,58,59,57],[60,60,64,65,64,64,65,64,64,64,64,64,64,62,62,60,59,59,59,59,60,61,62,61,62,61,59,58,58,58,58,57],[59,60,63,64,63,64,64,63,63,63,63,63,62,61,61,60,59,59,59,59,60,61,61,60,61,60,58,57,57,57,57,56],[59,60,62,64,63,63,64,63,64,63,63,63,62,61,61,60,59,59,60,60,61,61,61,60,61,60,59,58,57,57,58,57],[58,58,61,62,61,62,62,62,62,62,61,61,61,60,60,59,58,59,60,60,61,61,60,59,60,59,58,58,57,57,57,56],[59,60,62,63,62,63,63,63,63,63,62,62,62,61,61,61,60,60,61,61,62,62,61,60,60,60,59,59,58,57,58,56],[59,59,61,61,61,62,62,62,62,61,61,61,61,61,61,60,59,60,61,61,61,60,60,59,59,59,58,58,58,57,58,56]],"result":"63.08","message":"Created","code":"SUCCESS","success":true,"status":"OK","ContentType":"application/json"}

function toggle_heatmap() {
  $(this).attr('src', $(this).attr('src').replace("_raw.jpg", "_map.jpg"));
}
function toggle_image() {
  $(this).attr('src', $(this).attr('src').replace("_map.jpg", "_raw.jpg"));
}
function show_heatmap(){
  $('#heatmap').show();
  $('#imtest').fadeTo(500, 0.2)
}
function hide_heatmap(){
  $('#heatmap').hide();
  $('#imtest').fadeTo(500, 1)
}

// HTML5

function show_obj() {
  var top_margin = 25;
// https://stackoverflow.com/questions/318630/get-the-real-width-and-height-of-an-image-with-javascript-in-safari-chrome

 var img = $('#imtest')[0]; // Get my img elem
 width = img.clientWidth // display size
 height = top_margin + (img.naturalHeight) * width/img.naturalWidth;

 do_stretch = document.querySelector('#check_contrast_stretch').checked;

 mat = obj.local
//  for(var i = 0; i < mat.length; i++) {
//     for(var j = 0; j < mat[i].length; j++) {
//          mat[i][j] = Math.pow(mat[i][j]/100, 2)*100;
//     }
// }
 // https://stackoverflow.com/questions/30610523/reverse-array-in-javascript-without-mutating-original-array
 var data = [
   {
     z: mat.slice().reverse(),
     type: 'heatmap',
     opacity: 0.8,
     showscale: false
   }
 ];

  if(!do_stretch){
    data[0]['zmin'] = 0; //40
    data[0]['zmax'] = 100;
  }

  var layout = {
    height: height,
    width: width,
    autosize: true,
    margin: {
      l: 0,
      r: 0,
      b: 0,
      t: top_margin, // tooltip bar
      pad: 0
    },
    xaxis: {
      showgrid: false,
      zeroline: false,
      showline: false,
      ticks: '',
      showticklabels: false
    },
    yaxis: {
      showgrid: false,
      zeroline: false,
      showline: false,
      ticks: '',
      showticklabels: false
    },
  };
  Plotly.newPlot('heatmap', data, layout);

  var hist_data = [
    {
      x: [].concat(...mat.slice()),
      type: 'histogram',
  	  histnorm: 'probability',
  	  marker: {
          color: 'rgb(0,0,100)',
       },
    }
  ];

  var hist_layout = {
    height: 100,
    width: 400,
    autosize: true,
    margin: {
      l: 20,
      r: 20,
      b: 20,
      t: 0, // tooltip bar
      pad: 0
    },
  };

  // https://plot.ly/javascript/axes/
  if(!do_stretch){
    hist_layout['xaxis'] = {range: [0, 100]}
  }
  Plotly.newPlot('qualityHist', hist_data, hist_layout);


  // alert(obj.global);
  // $('#score').text(obj.result);

  // score = Math.pow(obj.result/100, 2)*100;
  score = obj.result;
  $('#score').width(score+'%').attr('aria-valuenow', score+'%');
  $('#score').text('Predicted Quality Score: ' + score);
  // to do, support multiple files
 // https://plot.ly/javascript/colorscales/
 //$('#imtest').height()  document.querySelector('#imtest').height
 //
}

$(document).ready(function(){
  // $("#imgUploaded").hover(hide_image, show_image);
  if( isMobile.any() ) {
    // mobile user
    $('.hovertoggle').bind('touchstart', toggle_heatmap).bind('touchend', toggle_image)
    // $('#image-with-heatmap').hover(hide_heatmap, show_heatmap);
    $('#image-with-heatmap').addClass("column");
    $('#btn_im_only').click(function(){ $('#imtest').css('opacity', '1'); $('#heatmap').css('opacity', '0');  }); // $('#imtest').fadeTo(1, 1);
    $('#btn_im_map').click(function(){ $('#heatmap').css('opacity', '0.8'); $('#imtest').css('opacity', '0.2')  }); // $('#imtest').fadeTo(1000, 0.2);
    $('#btn_map_only').click(function(){ $('#heatmap').css('opacity', '1'); $('#imtest').css('opacity', '0') });
  }
  else {
    $('.hovertoggle').hover(toggle_heatmap, toggle_image);
    // $('#image-with-heatmap').hover(show_heatmap, hide_heatmap);
    $('#btn_im_only').hover(function(){ $('#imtest').css('opacity', '1'); $('#heatmap').css('opacity', '0');  }); // $('#imtest').fadeTo(1, 1);
    $('#btn_im_map').hover(function(){ $('#heatmap').css('opacity', '0.8'); $('#imtest').css('opacity', '0.2')  }); // $('#imtest').fadeTo(1000, 0.2);
    $('#btn_map_only').hover(function(){ $('#heatmap').css('opacity', '1'); $('#imtest').css('opacity', '0') });
  }
  $('#imtest').fadeTo(1000, 0.2);
  $('#check_contrast_stretch').change(show_obj);
  // bootstrap button group active
  // https://jsfiddle.net/Behseini/NsQ2a/
  $(".btn-group > .btn").hover(function(){
      $(".btn-group > .btn").removeClass("active");
      $(this).addClass("active");
  });
  show_obj();
  // $('#check_contrast_stretch').prop( "checked", true );

  // ---------------------------------------------------------------------

  // const pond = FilePond.create(); // document.querySelector('.filepond');
  FilePond.setOptions({
      maxFiles: 1,
      server: {
          // url: 'http://localhost:8080',
          // url: 'https://10.157.89.130',
          // https gives ERR_CONNECTION_REFUSED
          url: 'https://paq2piq.appspot.com',
          process: {
              url: '/filepond', // roipool_model  sz
              // filepond2 to get squre scores
              method: 'POST',
              withCredentials: false,
              crossDomain: true,
              headers: {},
              timeout: 7000,
              onload: (response) => {
                 console.log(response);
                 obj = JSON.parse(response);
                 show_obj();
              },
              onerror: null,
              ondata: null,
          }
      }
  });
  FilePond.parse(document.body);
});


document.addEventListener('FilePond:loaded', e => {
    console.log('FilePond ready for use', e.detail);
    const inputElement = document.querySelector('#filepond');
    const pond = FilePond.create( inputElement );

    pond.on('addfile', (error, file) => {
        if (error) {
            console.log('Oh no');
            return;
        }
        //console.log('File added', file);
        f = window.URL.createObjectURL(pond.getFile().file)
        //console.log(pond.getFile().file)
        //console.log(f)
        // let img = new Image()
        img = document.querySelector('#imtest');
        img.src = f
        // img.onload = () => {
        //    // alert(img.width + " " + img.height);
        //    $('#image-with-heatmap').height(img.height);
        //    $('#image-with-heatmap').width(img.width);
        // }
    });
});
