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
obj = {"local":[[25,24,24,23,22,21,21,22,20,19,20,21,21,20,21,24,25,24,24,25,25,24,20,18,20,23,26,25,21,21,26,32],[23,23,22,21,20,18,18,18,17,15,17,19,18,16,18,21,22,22,22,22,23,21,17,15,17,20,23,21,18,18,23,30],[26,26,25,24,21,19,18,18,16,16,19,21,18,16,19,23,24,24,24,24,23,21,17,15,17,19,21,20,17,19,26,34],[28,29,28,27,22,18,18,16,15,18,24,24,19,16,18,23,24,24,24,25,26,23,18,16,16,17,18,17,16,19,27,36],[29,30,30,28,22,19,18,16,15,20,27,26,20,16,18,22,24,23,24,26,27,25,20,17,16,16,16,15,15,19,27,36],[31,32,31,29,24,21,20,18,17,21,27,27,21,16,18,23,25,25,27,30,31,30,25,21,19,17,17,15,15,20,28,36],[32,33,33,31,27,25,24,20,18,20,24,24,19,16,19,24,29,29,35,47,51,49,47,45,39,29,19,16,17,21,28,36],[32,33,33,31,28,26,24,21,17,17,20,20,17,16,19,25,31,32,37,48,51,49,50,50,46,37,23,18,19,22,28,36],[33,34,33,32,30,30,30,25,18,18,18,17,15,15,20,29,43,44,53,57,63,64,61,63,66,63,43,24,20,23,28,36],[32,33,33,32,30,31,32,26,19,17,16,15,14,14,20,32,47,48,53,51,59,63,57,59,64,66,51,29,23,23,28,36],[33,34,34,33,34,40,41,35,26,20,17,15,13,14,21,36,55,55,60,60,72,77,64,63,66,70,67,47,27,24,27,36],[35,37,38,37,48,65,67,61,52,40,22,16,14,16,24,40,61,60,64,65,76,80,65,56,59,63,68,62,38,26,26,35],[36,38,39,37,46,62,66,62,58,47,26,18,15,17,26,41,61,59,63,59,65,70,61,52,51,53,58,59,40,26,26,34],[38,41,43,50,58,67,75,79,80,69,40,20,17,19,28,45,67,61,67,64,66,71,67,55,52,52,59,65,48,28,27,34],[39,43,48,56,57,54,66,75,77,75,56,28,20,21,29,44,64,59,65,56,55,63,67,58,50,48,52,63,55,34,29,35],[39,41,47,50,48,43,52,60,62,65,56,30,22,22,28,38,54,54,60,50,49,54,59,55,49,46,49,56,53,37,31,35],[38,40,47,56,59,53,60,65,64,67,64,38,24,22,26,34,53,56,66,59,56,57,59,55,51,50,52,60,62,49,38,37],[35,34,40,53,60,54,58,61,61,61,63,50,28,21,22,27,37,41,55,62,63,57,51,49,50,51,51,54,58,61,58,49],[33,31,34,41,46,42,48,53,55,55,59,50,29,20,20,24,31,33,41,53,59,55,47,46,48,48,46,45,50,57,60,50],[32,29,29,34,41,40,47,51,53,53,59,55,31,21,20,25,32,34,41,56,67,61,48,48,49,49,46,44,47,55,62,60],[30,25,22,24,29,35,40,41,40,43,51,54,38,24,22,27,32,32,38,49,63,58,49,51,49,47,46,41,40,44,51,60],[28,23,21,22,26,32,37,36,36,39,46,50,38,26,25,28,32,32,37,44,53,52,49,51,48,46,46,40,36,38,44,52],[28,24,21,22,28,36,44,42,41,42,46,57,51,36,30,31,33,33,37,44,52,55,53,54,51,48,51,46,40,42,46,54],[28,25,23,23,28,43,56,52,47,46,45,65,70,57,43,38,35,33,35,39,50,57,56,54,50,49,54,54,47,45,53,55],[28,25,23,23,27,44,58,54,48,46,45,61,67,58,46,40,35,31,32,35,50,59,54,51,47,47,52,53,48,46,53,52],[29,27,24,24,28,50,63,57,50,50,55,70,69,65,60,45,35,30,31,33,51,61,56,52,48,47,52,55,51,50,57,54],[30,28,25,25,29,48,60,54,50,51,56,64,58,58,59,45,34,27,27,30,48,59,54,50,46,46,49,52,49,51,55,51],[31,30,27,26,31,51,60,54,52,53,58,65,59,61,65,51,34,27,26,29,49,60,56,52,47,47,51,54,51,54,56,52],[33,32,29,30,35,48,52,50,56,56,54,56,54,56,63,58,36,27,25,28,47,59,54,51,49,49,52,54,53,55,55,51],[33,33,31,31,36,45,47,49,55,55,50,52,51,54,58,55,36,28,26,28,42,54,51,51,50,49,50,53,53,53,52,50],[34,34,33,34,39,45,47,50,57,56,54,57,55,56,60,59,43,32,31,31,41,54,54,52,50,49,50,54,55,54,55,54],[32,32,31,31,34,37,37,42,45,44,44,47,45,44,46,47,37,30,30,28,32,38,40,40,41,41,42,44,45,43,45,45]],"result":"85.99","message":"Created","code":"SUCCESS","success":true,"status":"OK","ContentType":"application/json"};
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
 height = top_margin + img.clientHeight // (img.naturalHeight) * width/img.naturalWidth;
 $('#image-with-heatmap').height(height);
 $('#image-with-heatmap').width(width);

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
      l: 25,
      r: 25,
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
  $('#btn_im_map').trigger('mouseenter');
  $('#btn_im_map').trigger("click"); // mobile


  // alert(obj.global);
  // $('#score').text(obj.result);

  // score = Math.pow(obj.result/100, 2)*100;
  score = obj.result;
  $('#score').width(score+'%').attr('aria-valuenow', score+'%');
  // Predicted Quality Score: ' +
  $('#score').text(score);
  if (score > 80) {
    degree = 'Excellent'
  } else if (score > 60) {
    degree = 'Good'
  } else if (score > 40) {
    degree = 'Fair'
  } else if (score > 20) {
    degree = 'Poor'
  } else {
    degree = 'Bad'
  }
  $('#h1_score').text(degree);
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
    $('.advancedcfg').hide();
  }
  else {
    $('.hovertoggle').hover(toggle_heatmap, toggle_image);
    // $('#image-with-heatmap').hover(show_heatmap, hide_heatmap);
    $('#btn_im_only').hover(function(){ $('#imtest').css('opacity', '1'); $('#heatmap').css('opacity', '0');  }); // $('#imtest').fadeTo(1, 1);
    $('#btn_im_map').hover(function(){ $('#heatmap').css('opacity', '0.8'); $('#imtest').css('opacity', '0.2')  }); // $('#imtest').fadeTo(1000, 0.2);
    $('#btn_map_only').hover(function(){ $('#heatmap').css('opacity', '1'); $('#imtest').css('opacity', '0') });
  }
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
              url: '/filepond2', // roipool_model  sz
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

        document.querySelector('#imtest').src = f
        document.querySelector('#imraw').src = f
        $('#imtest').fadeTo(1000, 0.2);
        $('#heatmap').fadeTo(1000, 0);
        var img = $('#imraw')[0]; // Get my img elem
        width = img.clientWidth // display size
        height = top_margin + img.clientHeight
        $('#image-with-heatmap').height(height);
        $('#image-with-heatmap').width(width);
        $('btn_im_only').trigger('mouseenter');
    });
});
