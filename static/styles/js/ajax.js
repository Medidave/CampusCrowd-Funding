function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        // Check if name matches cookie name (don't include "=")
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = cookie.substring(name.length + 1);
          break;
        }
      }
    }
    return cookieValue;
  }


$(document).ready(function() {
    // $('.like-button').on('click', function(event) {  THIS CODE WAS WHAT WAS FIRST USED BUT AFTER WE CREATE THE ELEMENTS USING JS. THE STAR ICONS WERE NOT WORKING ANYMORE SO WE RESORTED ON DEFINING THE ON CLICK ON A PARENT CONTAINER SO THAT WE CAN TARGET THE RIGHT STAR WITH ITS ID WHEN CLICKED
    $('.campaigns').on('click', '.like-button', function(event) {

        event.preventDefault();
        var csrftoken = getCookie('csrftoken');

        var data = {};
        data['csrfmiddlewaretoken'] = csrftoken;

        var projectId = $(this).data('project-id');
        console.log(projectId)

        $.ajax({
            type: 'POST',
            // url: 'https://campuscrowd-8230c40f13a3.herokuapp.com//like_project/' + projectId + '/',
            url: '/like_project/' + projectId + '/',
            data: data,
            success: function(response) {
                if (response.status === 'success') {
                    var starsCount = response.stars;
                    $('#' + projectId).text(starsCount);
                    // likeButton.find('.likes-count').text(starsCount);  Both this Js code and the below work perfectly!!!
                    // alert(response.message);
                    if (response.message === 'Project stared'){
                        $('.' + projectId).addClass('liked-icon');
                    }else{
                        $('.' + projectId).removeClass('liked-icon');
                    }
                    
                } else {
                    alert('Error: ' + response.message);
                }
            },
            error: function(xhr, status, error) {
                alert('An error occurred: ' + error);
            }
        });
    });
});


// THE AJAX CODE FOR SENDING MAIL TO THE INVESTOR
$(document).ready(function() {
  $('.perks-container').on('click', '.send-mail', function(event) {

      event.preventDefault();
      var csrftoken = getCookie('csrftoken');

      var data = {};
      data['csrfmiddlewaretoken'] = csrftoken;

      var paymentId = $(this).data('payment-id');
      var likeButton = $(this);
      console.log(paymentId)
      console.log(likeButton)

      $.ajax({
          type: 'POST',
          url: '/send_mail/' + paymentId + '/',
          data: data,
          success: function(response) {
              if (response.status === 'success') {
                  
              console.log("DAVE THE CEO CEO")
                  
              } else {
                  alert('Error: ' + response.message);
              }
          },
          error: function(xhr, status, error) {
              alert('An error occurred: DAVE' + error);
          }
      });
  });
});


// AJAX CODE FOR SORTING THE CAMPAIGN
$(document).ready(function() {
    $('#sortBy').change(function() {
        console.log("Dave the ceo")
        var sortBy = $(this).val();

        var csrftoken = getCookie('csrftoken');

        var data = {};
        data['csrfmiddlewaretoken'] = csrftoken;

        
        $.ajax({
            url: '/sort_campaigns/' + sortBy + '/',  // The URL for (Sorting of campaigns) endpoint
            type: 'POST',
            data: data,

            success: function(data) {
                updateProjectList(data.project_data);
                
                // if (response.redirect_url) {
                //     // window.location.href = response.redirect_url;
                //     console.log(response.project_data)

                // }
            },
            error: function(xhr, status, error) {
                alert('An error occurred: ' + error);
            }
        });
    });
});

function updateProjectList(projects) {
    // Clear existing projects
    $('.campaigns').empty();

    // Append new sorted projects
    projects.forEach(project => {
        const suggestionHtml = `
        <div class="the-campaign">
          <div>
            <a href="/campaign/${project.id}/">
              <img src="${project.project_image}" alt="image" class="campaign-image">
            </a>
            <div class="project-texts">
              <div class="project-details">
                <a href="/campaign/${project.id}/">
                  <span>
                    <h3 class="project-name">${project.project_title}</h3>
                    <h5 class="project-desc">${project.brief_description}</h5>
                  </span>
                </a>
                ${project.authenticated ? `
                <button class="like-button" id="like-button" data-project-id="${project.id}">
                  <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 30 30" fill="none" class="${project.id} ${project.liked_project ? 'liked-icon' : ''}">
                    <path d="M12.541 4.08927C13.5469 1.97025 16.4531 1.97024 17.459 4.08926L19.1974 7.75147C19.5968 8.59294 20.3689 9.17617 21.262 9.31111L25.1492 9.89837C27.3983 10.2382 28.2964 13.1119 26.6689 14.7614L23.8561 17.612C23.2099 18.267 22.9149 19.2107 23.0675 20.1355L23.7315 24.1607C24.1157 26.4897 21.7645 28.2658 19.7528 27.1662L16.276 25.2658C15.4772 24.8291 14.5228 24.8291 13.724 25.2658L10.2472 27.1662C8.23549 28.2658 5.88428 26.4897 6.26848 24.1607L6.93249 20.1355C7.08505 19.2107 6.79014 18.267 6.14385 17.612L3.33109 14.7614C1.70358 13.1119 2.60166 10.2382 4.85083 9.89837L8.73797 9.31111C9.63111 9.17617 10.4032 8.59294 10.8026 7.75147L12.541 4.08927Z" stroke="#28303F" stroke-width="1.5" stroke-linejoin="round"/>
                  </svg>
                  <span class="likes-count" id="${project.id}">${project.project_stars}</span>
                </button>` : `
                <button class="flex-btn">
                  ${project.project_stars > 0 ? `
                  <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 30 30" fill="#00FF66">
                    <path d="M12.541 4.08927C13.5469 1.97025 16.4531 1.97024 17.459 4.08926L19.1974 7.75147C19.5968 8.59294 20.3689 9.17617 21.262 9.31111L25.1492 9.89837C27.3983 10.2382 28.2964 13.1119 26.6689 14.7614L23.8561 17.612C23.2099 18.267 22.9149 19.2107 23.0675 20.1355L23.7315 24.1607C24.1157 26.4897 21.7645 28.2658 19.7528 27.1662L16.276 25.2658C15.4772 24.8291 14.5228 24.8291 13.724 25.2658L10.2472 27.1662C8.23549 28.2658 5.88428 26.4897 6.26848 24.1607L6.93249 20.1355C7.08505 19.2107 6.79014 18.267 6.14385 17.612L3.33109 14.7614C1.70358 13.1119 2.60166 10.2382 4.85083 9.89837L8.73797 9.31111C9.63111 9.17617 10.4032 8.59294 10.8026 7.75147L12.541 4.08927Z" stroke="#28303F" stroke-width="1.5" stroke-linejoin="round"/>
                  </svg>` : `
                  <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 30 30" fill="none">
                    <path d="M12.541 4.08927C13.5469 1.97025 16.4531 1.97024 17.459 4.08926L19.1974 7.75147C19.5968 8.59294 20.3689 9.17617 21.262 9.31111L25.1492 9.89837C27.3983 10.2382 28.2964 13.1119 26.6689 14.7614L23.8561 17.612C23.2099 18.267 22.9149 19.2107 23.0675 20.1355L23.7315 24.1607C24.1157 26.4897 21.7645 28.2658 19.7528 27.1662L16.276 25.2658C15.4772 24.8291 14.5228 24.8291 13.724 25.2658L10.2472 27.1662C8.23549 28.2658 5.88428 26.4897 6.26848 24.1607L6.93249 20.1355C7.08505 19.2107 6.79014 18.267 6.14385 17.612L3.33109 14.7614C1.70358 13.1119 2.60166 10.2382 4.85083 9.89837L8.73797 9.31111C9.63111 9.17617 10.4032 8.59294 10.8026 7.75147L12.541 4.08927Z" stroke="#28303F" stroke-width="1.5" stroke-linejoin="round"/>
                  </svg>`}
                  <span class="likes-count" id="${project.id}">${project.project_stars}</span>
                </button>`}
              </div>
              <a href="/campaign/${project.id}/">
                <div class="secod-div">
                  <div class="project-owner-details">
                    <img src="${project.project_owner_image}" alt="image" class="project-owner-image">
                    <span class="name-description">
                      <h5>${project.project_owner_name}</h5>
                      <p>${project.project_owner_program}</p>
                      <p>${project.project_owner_Abbr}</p>
                    </span>
                  </div>
                  <span class="perker-counts">
                    <h1>${Math.floor(project.percentage_funded)}%</h1>
                    <div class="progress-bar-container">
                      <div class="progress-bar" style="width: ${Math.floor(project.percentage_funded)}%;"></div>
                    </div>
                    <p class="the-ps">Funded</p>
                  </span>
                </div>
              </a>
              <a href="/campaign/${project.id}/">
                <div class="last-div">
                  <span>
                    <span class="lg">GHC</span>
                    <h1 class="inline">${project.amount_raised}</h1>
                    <p class="the-ps">Raised</p>
                  </span>
                  <span class="perker-counts">
                    <h1>${project.payment_count}</h1>
                    <p class="the-ps">${project.payment_count === 1 ? 'Perker' : 'Perkers'}</p>
                  </span>
                  <span class="perker-counts">
                    <h1>${project.target_funding_period_in_days}</h1>
                    <p class="the-ps">Days Left</p>
                  </span>
                </div>
              </a>
            </div>
          </div>   
        </div>`;

        $('.campaigns').append(suggestionHtml);
    });
}


// THE AJAX CODE THAT HANDLES ASYNCHRONOUS COMMUNICATION WITH THE SERVER FOR SUGGESTIONS
$(document).ready(function() {
  $('.the-forms').on('click', '.suggestions-btn', function(event) {

      event.preventDefault();
      var csrftoken = getCookie('csrftoken');

      const textarea = document.getElementById('suggestion-content');
      const content = textarea.value;

      var data = {};
      data['csrfmiddlewaretoken'] = csrftoken;
      data['content'] = content;

      var projectId = $(this).data('project-id');

      $.ajax({
          type: 'POST',
          url: '/users/suggestions/' + projectId + '/',
          data: data,
          success: function(response) {
              if (response.status === 'success') {
               updateSuggestionList(response.suggestions);
               textarea.value = '';
              }else if(response.status === 'fail') {
                alert("Error: Please enter a suggestion in the input box!" )   
              }else {
                alert('Error: ' + response.message);
            }
                
          },
          error: function(xhr, status, error) {
              alert('An error occurred: ' + error);
          }
      });
  });
});

function updateSuggestionList(suggestions) {
  // Clear existing projects
  $('.loop-suggestions').empty();

  // Append new sorted projects
  suggestions.forEach(suggestion => {
      const suggestionHtml = `
      <div class="suggestions-container">
        <span class="suggestions">
          <img src="${suggestion.user_image}" alt="Default Image" class="room-host-image image-image">
          <span class="hint-names">
            <h2 class="">${suggestion.first_name} ${suggestion.last_name}</h2>
            <p class="green">${suggestion.timestamp}</p>
          </span>
        </span>
        <p>${suggestion.content}</p>
      </div>`;

      $('.loop-suggestions').append(suggestionHtml);
  });
}



// THE BELOW SCRIPTS ARE THE CODE FOR THE TOPIC AND THE PARTICIPANTS  BUTTONS AT THE CHATROOM

const openButtonParticipants = document.getElementById('open-button-participants');
const sideBarParticipants = document.getElementById('sidebar-participants');
const closeButtonParticpants = document.getElementById('close-participants');

openButtonParticipants.addEventListener("click", () => {
  sideBarParticipants.classList.toggle("open-sidbar-for-participants")
  
  document.onclick = function (e){
    if (!sideBarParticipants.contains(e.target) && !openButtonParticipants.contains(e.target)){
      sideBarParticipants.classList.remove("open-sidbar-for-participants");
  
    }
  }
  
}
  );

closeButtonParticpants.addEventListener("click", () => {
  sideBarParticipants.classList.toggle("open-sidbar-for-participants");
});

// THE BELOW CODE IS RESPONSIBLE FOR MAKING THE TEXTAREA INPUT GROW AS THE CONTENT OF THE TEXT GROWS
const textarea = document.getElementById('myTextarea');

textarea.addEventListener('input', () => {
  textarea.style.height = 'auto';
  textarea.style.height = textarea.scrollHeight + 'px';
});


// MAKE THE SCROLL BAR OF THE CHAT BOX TO DISPLAY THE CURRENT TEXT ALWAYS 
window.onload = function() {
  const chatBox = document.getElementById("chat-box");
  if (chatBox) {
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
  }
};