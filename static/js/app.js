document.addEventListener("DOMContentLoaded", function () {
  const composeForm = document.getElementById("compose-form");
  if (composeForm) {
    composeForm.addEventListener("submit", function (event) {
      const recipientField = document.querySelector('[name="recipients"]');
      if (!recipientField) return;
      const lines = recipientField.value.split("\n").map(line => line.trim()).filter(Boolean);
      if (lines.length > 10) {
        event.preventDefault();
        alert("Please send to a maximum of 10 recipients per batch.");
      }
    });
  }
});
