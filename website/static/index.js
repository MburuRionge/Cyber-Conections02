// Define a function to delete a note by its ID
function deleteNote(noteId) {
    // Use the fetch API to send a request to the server
    fetch("/delete-note", {
        method: "POST",  // Specify the request method as POST
        body: JSON.stringify({ noteId: noteId }),  // Send the note ID as JSON in the request body
    }).then((_res) => {
        // Once the server responds, reload the current page to reflect the changes
        window.location.href = "/";
    });
}
