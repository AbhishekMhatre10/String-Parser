function parseSentence() {
    var sentence = document.getElementById('sentenceInput').value;
    fetch('/parse', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({"sentence": sentence}),
    })
    .then(response => response.json())
    .then(data => {
        // Assuming the backend returns a JSON object with a key that holds the result
        document.getElementById('parseResult').innerText = JSON.stringify(data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
