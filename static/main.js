$(function () {
    var syncClient;
    var syncStream;
    var message = document.getElementById('message');
    var text_area = document.getElementById('text_area');
    var select_element = document.getElementById('select')
    var background_color;


    $.getJSON('/token', function(tokenResponse) {
        syncClient = new Twilio.Sync.Client(tokenResponse.token, { logLevel: 'info' });

        // create the stream object
        syncClient.stream('messageData').then(function(stream) {
            syncStream = stream;
            // listen update and sync drawing data
            syncStream.on('messagePublished', function(event) {
                console.log('syncStream:',event.message.value);
                syncDrawingData(event.message.value);


            });
        });
    });
    // Write the code here
    function syncDrawingData(data) {
        document.getElementById('text_area').value = data.textarea_value;
        document.getElementById('text_area').style.backgroundColor = data.textarea_color;
    }


    function messageSync(){
	text = document.getElementById("text_area").value;

    setTimeout(function(){
        SettingSyncData()
        },
        1700);

}
    // Write the code here
    function SettingSyncData(){
    syncStream.publishMessage({ 
            textarea_color:background_color,
            textarea_value:text
        });
    }
    // Write the code here
    function select_color(){
        selected_color = document.getElementById("select").value;
        background_color = selected_color;

    }
    // Write the code here
    text_area.addEventListener("keyup", messageSync) 
    select_element.addEventListener("change", select_color)
    

});
