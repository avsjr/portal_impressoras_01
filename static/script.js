console.log('Script loaded successfully');

document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM loaded successfully');

    function adicionarImpressora(printerName) {
        console.log('Printer name:', printerName);

        fetch('/adicionarImpressora', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'printerName': printerName })
        })
        .then(response => {
            if (response.ok) {
                console.log('Printer added successfully');
                alert('Impressora adicionada com sucesso!');
            } else if (response.status === 404) {
                console.log('Printer not found');
                alert('Impressora não encontrada.');
            } else {
                console.log('Failed to add printer.');
                alert('Não foi possível adicionar a impressora.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error: ' + error);
        });
    }

    let btnAdicionar = document.querySelectorAll('.btn-adicionar');

    btnAdicionar.forEach(button => {
        button.addEventListener('click', function () {
            let printerNameElement = this.parentElement.querySelector('.printer-name.visually-hidden');
            if (printerNameElement) {
                let printerName = printerNameElement.innerText.trim();
                adicionarImpressora(printerName);
            } else {
                console.error('Printer name element not found');
                alert('Elemento do nome da impressora não encontrado');
            }
        });
    });
});
