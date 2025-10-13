document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('form.add-to-cart-form').forEach(function(form) {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      const formData = new FormData(form);
      fetch(form.action, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          console.log(data.message); // Or update the cart count, etc.
        }
      });
    });
  });
});

console.log("here")