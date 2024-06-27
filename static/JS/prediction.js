function confirmationPhrase(containerInput1Id, containerInput2Id, containerMsgId, inputMId, inputTId)
{
    const containerS1 = document.getElementById(containerInput1Id);
    const containerS2 = document.getElementById(containerInput2Id);

    const containerM1 = document.getElementById(inputMId);
    const containerT1 = document.getElementById(inputTId);

    containerS1.addEventListener('change', function() 
    {
        if (containerM1.innerText != '/' && containerT1 .innerText != '/') 
            {
                const home_score = (parseInt(containerM1.textContent) + parseInt(containerT1.textContent))/2;
                const away_score = parseInt(containerT1.textContent) - home_score;
                
                var containerMsg = $(document.getElementById(containerMsgId));
                containerMsg.empty();

                var html = '<div> Prediction: ' + home_score + ' - ' + away_score + '</div>';

                containerMsg.append(html);
            } 
    });

    containerS2.addEventListener('change', function() 
    {
        if (containerM1.innerText != '/' && containerT1 .innerText != '/') 
            {
                const home_score = (parseInt(containerM1.textContent) + parseInt(containerT1.textContent))/2;
                const away_score = parseInt(containerT1.textContent) - home_score;
                
                var containerMsg = $(document.getElementById(containerMsgId));
                containerMsg.empty();

                var html = '<div> Prediction: ' + home_score + ' - ' + away_score + '</div>';

                containerMsg.append(html);
            } 
    });
}

confirmationPhrase('content-predic1-1', 'content-predic1-2', 'confirmationMsg1', 'rangeValueM1', 'rangeValueT1');
confirmationPhrase('content-predic2-1', 'content-predic2-2', 'confirmationMsg2', 'rangeValueM2', 'rangeValueT2');

// Quand j'avais utilisé des select box
/*function selectBoxPredic(container)
{
    // Définir la plage des marges de points
    const maxMargin = 50.5;
    const increment = 0.5; // Incrément des options

    const containerD = document.getElementById(container);
    const typePredic = containerD.querySelector('.title-prediction');
    const dropdowns = containerD.querySelector('.container-select');
    const containerLi = dropdowns.querySelector('.val-scrollbar');
    
    if (typePredic.textContent == 'Margin:')
    {
        for (let i = -maxMargin; i <= maxMargin; i += increment) 
        {
            if (!Number.isInteger(i))
            {
                let li = document.createElement('li');
                li.textContent = i;
                containerLi.appendChild(li);
            }
        }
    }
    else if (typePredic.textContent == 'Total:')
    {
        for (let i = 0; i <= maxMargin; i += 1) 
        {
            let li = document.createElement('li');
            li.textContent = i;
            containerLi.appendChild(li);
        }
    }
    
}

function confirmationPhrase(containerConfrontationId, containerSelect1Id, containerSelect2Id, containerMsgId)
{
    const containerS1 = document.getElementById(containerSelect1Id);
    const containerS2 = document.getElementById(containerSelect2Id);

    const containerLiS1 = containerS1.querySelector('.val-scrollbar');
    const containerLiS2 = containerS2.querySelector('.val-scrollbar');  
    console.log(containerLiS1);
    const selectedS1 = containerS1.querySelector('.selected');
    const selectedS2 = containerS2.querySelector('.selected');
    
    // Ajouter les écouteurs d'événements sur les deux éléments
    containerLiS1.addEventListener('click', function() 
    {   
        console.log(selectedS1.textContent);
        console.log(selectedS1.textContent);
        console.log(selectedS2.textContent);
        if (selectedS1.textContent.length >= 1 && selectedS2.textContent.length >= 1) 
        {
            
        
            const containerConf = document.getElementById(containerConfrontationId);
            const containerTeam = containerConf.querySelectorAll('.container-team');
            var home_score = 0;

            if(parseFloat(selectedS1.textContent) >= 0)
            {
                home_score = (Math.ceil(parseFloat(selectedS1.textContent)) + parseInt(selectedS2.textContent))/2;
            }
            else
            {
                home_score = (Math.floor(parseFloat(selectedS1.textContent)) + parseInt(selectedS2.textContent))/2;
            }
            
            const away_score = parseInt(selectedS2.textContent) - home_score;
          
            const homeTeam = containerTeam[0].querySelector('.name-team').textContent;
            const awayTeam = containerTeam[1].querySelector('.name-team').textContent;
            
            var containerMsg = $(document.getElementById(containerMsgId));
            containerMsg.empty();

            var html = '<div> Prediction: ' + Math.floor(home_score) + ' - ' + Math.floor(away_score) + '</div>';

            containerMsg.append(html);
        }
    });

    containerLiS2.addEventListener('click', function() 
    {
        if (selectedS1.textContent.length >= 1 && selectedS2.textContent.length >= 1)
        {
            const containerConf = document.getElementById(containerConfrontationId);
            const containerTeam = containerConf.querySelectorAll('.container-team');
            var home_score = 0;

            if(parseFloat(selectedS1.textContent) >= 0)
            {
                home_score = (Math.ceil(parseFloat(selectedS1.textContent)) + parseInt(selectedS2.textContent))/2;
            }
            else
            {
                home_score = (Math.floor(parseFloat(selectedS1.textContent)) + parseInt(selectedS2.textContent))/2;
            }
            
            const away_score = parseInt(selectedS2.textContent) - home_score;
          
            const homeTeam = containerTeam[0].querySelector('.name-team').textContent;
            const awayTeam = containerTeam[1].querySelector('.name-team').textContent;
            
            var containerMsg = $(document.getElementById(containerMsgId));
            containerMsg.empty();

            var html = '<div> Prediction: ' + Math.floor(home_score) + ' - ' + Math.floor(away_score) + '</div>';

            containerMsg.append(html);
        }
    });
}


selectBoxPredic('content-predic1-1');
confirmationPhrase('confrontation-predic', 'content-predic1-1', 'content-predic1-2', 'confirmationMsg1');
selectBoxPredic('content-predic1-2'); */