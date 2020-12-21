let ex_file;

function printLoading(){
    var str = "";
    str += "<div class=\"loading\">";
    str += "<span>L</span>";
    str += "<span>O</span>";
    str += "<span>A</span>";
    str += "<span>D</span>";
    str += "<span>I</span>";
    str += "<span>N</span>";
    str += "<span>G</span>";
    str += "</div>";

    $("body").append(str);
}

function removeLoading(){
    $(".loading").remove();
    $(".uploading").remove();
    $(".downloading").remove();
}

function save_file(event){
    ex_file=event.target.files[0];
    console.log("현재파일: ", ex_file);
}
window.onload=function(){
    
    // console.log("csrf 결과값", temp);
    let prediction_button=document.getElementById("prediction");
    let file_button=document.getElementById("file");

    file_button.addEventListener("change",save_file);

    prediction_button.addEventListener("click",function(){
        console.log("예측 버튼을 눌렀습니다.");
        let formData = new FormData();

        formData.append('file', ex_file);
        
        formData.append('csrfmiddlewaretoken', temp);

        $.ajax({
            url: "dataTransmit/",
            type: "post",
            data : formData,
            processData:false,
			contentType:false,
            async: true,
            beforeSend: function(){
                printLoading();
            },
            success: function (result) {

                if(result.error==='no')
                {
                    const json_data = JSON.parse(result.json_data);
                    const predicted_data = result.predicted_data;
                    const columns = Object.keys(json_data);

                    // 데이터 전처리 및 차트 디스플레이
                    chart_prediction(json_data, predicted_data);

                    // 예측한 데이터를 동적으로 html document에 표시
                    let template = '<p></p>';
                    for(let i=1; i<columns.length; i++) {
                        template += '<p>';
                        template += columns[i];
                        template += ' 예측 값: ';
                        template += predicted_data[i-1];
                        template += '</p>';
                    }
                    $('#predicted_display_area').html(template);
                }else{
                    console.log("에러 발생!!  :" + result.message);
                    document.getElementById("error_contents").innerHTML="<div align='center'>Error Helper</div><br><br><b>=></b> "+result.message;
                    openModal('modal1')
                }

            },
            error: function (err) {
                removeLoading();
            },
            complete: function(){
                removeLoading();
            }
        });
    })
      
      $("#modal, .close").on('click',function(){
        $("#modal").fadeOut(300);
        $(".modal-con").fadeOut(300);
      });
}
function openModal(modalname){
    document.get
    $("#modal").fadeIn(300);
    $("."+modalname).fadeIn(300);
}