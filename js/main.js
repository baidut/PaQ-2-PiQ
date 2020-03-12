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
obj = {"global_score":78,"normalized_global_score":84,"local_scores":[[53,52,52,51,51,50,49,51,50,51,53,53,53,50,49,51,53,51,51,56],[53,53,51,49,48,47,48,50,47,50,52,52,52,48,46,48,51,48,51,57],[55,54,52,49,48,46,50,52,47,49,52,53,53,50,47,47,49,47,51,58],[56,56,53,50,49,48,52,54,48,49,53,55,56,55,51,49,48,46,51,58],[57,56,55,53,51,49,50,52,48,50,55,62,63,63,61,59,49,47,52,58],[57,57,56,55,54,49,48,48,46,52,61,66,66,68,66,69,60,52,53,58],[57,57,58,59,60,53,49,46,45,55,64,68,69,71,66,70,67,61,53,58],[59,58,63,67,69,63,58,47,46,57,66,69,70,71,64,67,68,67,53,57],[60,60,67,67,72,71,69,50,48,59,67,69,67,70,64,65,65,68,54,57],[61,62,68,64,70,70,71,54,50,59,67,68,64,68,65,64,63,68,57,57],[60,62,68,64,68,67,70,59,52,55,64,69,64,67,64,64,63,68,63,58],[58,59,68,64,67,66,68,63,52,52,58,68,66,65,62,63,63,65,67,62],[55,55,60,59,63,64,66,64,53,51,56,65,68,66,62,63,61,62,67,66],[53,51,54,59,63,60,64,67,63,54,57,62,67,67,64,63,63,62,63,66],[53,51,53,61,67,62,63,67,70,61,57,59,63,66,64,63,64,64,64,64],[54,53,54,63,69,63,66,68,70,67,58,56,63,67,63,63,63,65,65,64],[55,54,55,63,68,63,67,67,68,69,57,54,63,67,63,62,63,64,66,63],[57,55,57,62,65,64,66,65,65,69,58,54,62,67,63,63,63,65,65,63],[57,56,59,61,64,65,66,65,66,68,60,57,60,66,63,63,63,65,65,64],[56,56,57,58,60,61,62,62,62,63,58,56,56,60,59,60,60,61,62,61]],"normalized_local_scores":[[20,19,18,15,15,14,12,16,13,17,20,20,21,14,10,15,22,15,17,30],[21,21,16,11,9,6,7,14,6,13,20,19,19,9,4,9,16,9,15,32],[26,25,18,11,7,4,12,19,6,11,20,21,22,14,6,7,10,4,15,34],[29,29,21,15,10,8,18,23,7,12,21,27,29,25,16,10,8,3,16,34],[31,31,25,20,16,10,14,19,7,14,26,46,48,49,43,37,11,6,19,35],[31,31,29,27,25,10,8,8,4,19,41,57,57,62,57,65,41,18,21,34],[33,32,34,38,40,22,11,4,0,26,51,61,63,70,57,66,60,43,21,34],[37,36,49,58,64,49,36,7,2,32,56,64,66,70,52,59,60,59,22,33],[41,41,60,60,71,68,65,14,9,38,60,64,59,66,51,53,54,62,25,32],[42,46,61,50,66,66,69,24,14,37,58,62,51,63,53,49,49,62,33,33],[40,45,61,50,61,58,66,36,18,27,50,64,52,57,51,50,49,60,48,36],[34,38,60,50,58,56,62,47,20,18,36,61,57,53,46,49,48,54,60,46],[28,26,40,38,49,49,56,51,22,16,29,52,60,55,45,47,44,45,57,55],[22,15,23,37,47,41,50,58,49,24,31,45,57,58,50,49,48,45,49,56],[22,17,22,41,58,45,47,58,66,43,33,37,47,56,51,48,51,51,50,51],[25,20,23,47,64,47,55,62,67,60,33,30,48,57,49,47,49,52,54,50],[28,23,27,48,60,49,57,58,61,64,32,25,47,58,48,46,48,51,55,49],[31,26,32,46,54,52,55,52,54,63,34,25,44,58,48,48,49,52,54,48],[33,30,37,43,51,53,56,53,55,62,41,31,39,56,49,49,47,52,54,50],[30,28,33,35,41,43,45,44,45,48,35,28,29,41,38,40,40,43,45,43]],"category":"Excellent"}
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

 mat = obj.normalized_local_scores
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
  score = obj.normalized_global_score;
  $('#score').width(score+'%').attr('aria-valuenow', score+'%');
  // Predicted Quality Score: ' +
  $('#score').text(score);
  $('#h1_score').text(obj.category);
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
              url: '/filepond',
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
