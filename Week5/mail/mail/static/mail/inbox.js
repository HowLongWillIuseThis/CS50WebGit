document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#submit_button').onclick = () => 
  {
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-recipients').value;
    const body = document.querySelector('#compose-body').value;
    fetch('/emails', 
    {
      method:'POST',
      body: JSON.stringify(
        {
          recipients: recipients,
          subject: subject,
          body: body
        })
    })
    .then(response => response.json())
    .then(result =>
      {
        console.log(result);
      })
    .catch(error =>
      {
        console.log(error);
      });
      load_mailbox('sent');
  };


  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function reply_email(email_id)
{
  compose_email();
  fetch(`emails/${email_id}`)
  .then(response => response.json())
  .then(result => 
    {
      document.querySelector('#compose-recipients').value = `${result.sender}`;
      document.querySelector('#compose-subject').value = `Re: ${result.subject}`;
      document.querySelector('#compose-body').value = `On ${result.timestamp} ${result.recipients} wrote:`;
    })
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`emails/${mailbox}`)
  .then(response => response.json())
  .then(result => 
  {
    console.log(result)
    result.forEach(element => 
      {
        const hello = document.createElement('div')
        hello.className = "email";
        console.log(element.sender)
        let inside_div = document.createElement('div')
        inside_div.append(element.timestamp);
        inside_div.style.float = "right";
        hello.append(`Sender: ${element.sender}    Subject: ${element.subject}`)
        hello.appendChild(inside_div)
        if(element.read === true)
        {
          hello.style.color = "LightGray";
          hello.style.borderColor = "LightGray";
        }
        hello.addEventListener('click', () =>
        {
          fetch(`emails/${element.id}`)
          .then(response => response.json())
          .then(result =>
            {
              document.querySelector('#emails-view').innerHTML = '';
              const email_detail = document.createElement('div');
              email_detail.id = "email_detail";

              const archive = document.createElement('div');
              archive.style.cssFloat = "right";
              archive.innerHTML = "Archive ";
              const archive_check = document.createElement('input');
              archive_check.id = "archive_check";
              archive_check.setAttribute('type', 'checkbox');

              archive_check.addEventListener('click', () =>
              {
                let is_archived = result.archived;
                console.log(is_archived);
                if(is_archived === true)
                {
                  is_archived = false;
                }
                else
                {
                  is_archived =true;
                }
                console.log(is_archived);
                fetch(`emails/${element.id}`, {
                  method: 'PUT',
                  body: JSON.stringify({
                      archived: is_archived
                  })
                });
                load_mailbox('inbox');
              });

              const reply_button = document.createElement('button');
              reply_button.id = "reply_button";
              reply_button.innerHTML = "Reply";
              reply_button.addEventListener('click', function()
              {
                reply_email(element.id);
              });

              archive.appendChild(archive_check);
              email_detail.appendChild(archive);
              
              email_detail.insertAdjacentHTML('beforeend', 
              `              FROM: ${result.sender}
              TO: ${result.recipients}
              SUBJECT: ${result.subject}
              TIMESTAMP: ${result.timestamp}`);
              
              email_detail.appendChild(reply_button);
              document.querySelector('#emails-view').appendChild(email_detail);
              document.querySelector('#emails-view').insertAdjacentHTML('beforeend', `<hr /> ${result.body}`);

              if(result.archived === true)
              {
                document.querySelector('#archive_check').checked = true;
              }

              fetch(`emails/${element.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    read: true
                })
              })
              .catch(error =>
                {
                  console.log(error);
                });


            })
          .catch(error =>
            {
              console.log(error)
            });
        });
        document.querySelector('#emails-view').appendChild(hello);
      })
  })
  .catch(error =>
    {
      console.log(`This does not exist. ${error}`)
    });
}