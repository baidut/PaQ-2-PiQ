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
var obj = {"local":[[24,22,24,25,25,26,26,26,25,23,22,24,29,31,36,40,41,40,34,30,30,28,27,26,26,25,25,26,27,27,29,29],[23,22,23,25,25,25,25,24,23,21,20,23,28,30,34,37,38,37,34,30,29,27,26,25,25,24,24,25,26,26,28,28],[27,26,30,31,31,31,29,29,27,26,26,32,38,37,40,42,42,44,42,37,38,38,36,33,33,31,30,32,32,31,33,31],[28,28,32,33,32,32,30,29,28,28,28,35,41,39,41,42,42,44,44,39,41,41,39,36,36,34,33,34,34,33,34,32],[30,30,35,34,32,32,32,31,31,33,34,41,45,43,44,43,42,45,45,41,44,46,45,42,41,38,36,37,36,34,34,32],[31,31,35,33,31,31,32,32,31,34,36,43,46,43,44,43,40,43,43,41,44,47,46,44,43,39,37,38,36,34,34,31],[31,31,35,33,30,31,33,34,35,42,44,49,50,48,48,44,41,43,43,41,44,47,48,46,46,44,42,42,38,35,35,31],[30,30,34,32,29,31,34,35,37,44,46,50,51,49,49,44,40,41,40,39,42,46,48,46,47,45,43,43,39,35,35,31],[30,31,35,32,30,32,37,38,40,44,44,49,51,50,49,44,40,41,40,39,42,46,48,46,47,46,45,45,41,36,37,32],[30,31,35,33,30,32,38,39,40,39,39,43,48,48,46,42,39,39,38,37,41,44,45,44,44,44,44,44,41,37,37,32],[31,32,36,34,32,35,39,39,40,39,38,43,46,45,44,41,37,38,38,38,42,45,45,43,44,44,44,44,42,39,41,34],[31,32,37,35,33,36,38,38,37,36,36,39,41,39,38,36,35,36,38,38,42,43,41,40,40,41,42,42,42,40,41,35],[31,32,38,37,34,37,41,40,39,38,37,40,41,39,38,36,34,36,38,39,43,44,41,39,39,40,40,41,42,41,43,36],[31,32,38,38,36,39,42,42,43,43,42,43,43,41,40,38,36,37,38,39,43,47,42,36,35,35,35,38,41,41,43,36],[31,32,37,38,36,39,42,42,44,44,43,44,44,43,42,39,38,38,38,38,42,46,42,36,35,33,32,36,40,40,41,35],[33,33,39,40,38,41,42,41,44,44,42,44,46,46,46,46,43,42,38,36,41,48,46,39,37,34,33,36,40,40,42,37],[33,34,39,40,39,41,41,39,40,40,39,41,46,47,48,48,45,43,36,34,39,47,47,41,38,33,32,33,37,38,40,36],[35,36,43,43,41,42,42,40,39,38,37,39,45,47,48,48,45,43,36,34,38,46,47,42,41,36,34,34,37,37,40,36],[36,37,44,44,41,42,41,39,37,34,31,34,42,45,47,46,42,40,35,33,36,40,43,42,41,37,35,34,34,34,36,33],[39,41,49,49,44,46,44,41,39,33,31,33,41,44,47,45,41,39,34,32,35,39,43,43,44,40,36,36,34,34,36,33],[40,42,50,50,45,47,45,42,39,32,29,31,37,40,43,42,38,36,32,31,32,34,40,42,44,41,37,36,33,33,34,32],[44,47,56,55,50,51,49,46,43,35,31,33,38,40,43,42,38,36,32,31,32,34,41,44,49,47,42,40,35,33,35,33],[43,46,55,55,51,52,50,47,45,37,33,34,37,38,40,39,36,35,31,30,30,33,41,44,49,49,44,41,35,33,35,33],[44,47,58,59,54,57,55,52,50,43,40,40,41,40,41,39,36,35,32,31,32,36,43,45,51,50,45,44,38,35,37,34],[42,45,56,58,54,57,56,53,51,46,43,43,42,39,39,37,35,34,31,31,33,37,43,45,49,48,44,43,39,36,38,34],[42,45,57,60,55,58,58,55,55,52,50,53,51,46,45,39,37,36,34,34,37,43,47,46,49,48,43,42,39,37,38,35],[41,43,53,57,55,56,57,54,56,55,53,55,53,48,47,41,38,38,38,38,42,45,47,44,47,44,39,37,36,35,37,34],[39,41,49,53,51,53,53,50,52,52,51,51,49,45,45,41,38,39,39,38,42,44,45,42,44,42,37,35,33,33,35,33],[39,41,49,53,51,52,53,51,53,53,50,50,48,45,46,42,39,40,42,42,45,46,45,43,44,42,38,36,34,34,36,33],[36,37,45,48,46,48,49,48,49,48,46,46,44,43,43,40,38,39,42,42,45,45,43,40,41,40,37,36,34,33,35,31],[40,41,48,49,47,50,52,51,51,50,47,48,47,46,46,43,41,42,45,45,47,47,45,42,42,41,38,39,37,35,37,33],[39,40,45,46,44,47,49,48,48,46,43,45,45,44,44,42,40,41,43,44,44,43,42,40,40,38,37,37,36,34,35,32]],"result":"35.02","message":"Created","code":"SUCCESS","success":true,"status":"OK","ContentType":"application/json"};

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
