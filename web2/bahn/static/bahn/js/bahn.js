var segmentCounter = 1

function addSegment() {
    console.log('Segment hinzufügen...')
    segmentCounter += 1;
    $('.segmentformular').append('\
            <label for="start' + segmentCounter + '">Start:</label>\
            <input type="text" name="start' + segmentCounter + '" id="start' + segmentCounter + '">\
            <label for="ziel' + segmentCounter + '">Ziel:</label> \
            <input type="text" name="ziel' + segmentCounter + '" id="ziel' + segmentCounter + '"></br>\
    ');
}