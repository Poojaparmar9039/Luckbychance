document.addEventListener("DOMContentLoaded", function() {
  // Subcategory loading
  document.getElementById("id_category").addEventListener("change", function () {
  const subcatSelect = document.getElementById("id_subcategory");
  const loadingIndicator = document.getElementById("subcat-loading");
  const form = document.getElementById("ad-form");
  const url = form.dataset.subcatUrl + "?category_id=" + this.value;

  subcatSelect.innerHTML = "";
  subcatSelect.disabled = true;
  loadingIndicator.style.display = "inline";

  fetch(url)
    .then(response => response.json())
    .then(data => {
      const defaultOption = document.createElement("option");
      defaultOption.value = "";
      defaultOption.textContent = "Select a subcategory";
      subcatSelect.appendChild(defaultOption);

      data.forEach(function (item) {
        const option = document.createElement("option");
        option.value = item.id;
        option.textContent = item.name;
        subcatSelect.appendChild(option);
      });

      subcatSelect.disabled = false;
    })
    .catch(() => {
      alert("Error loading subcategories. Please try again.");
    })
    .finally(() => {
      loadingIndicator.style.display = "none";
    });
});

  // File upload preview
  document.getElementById("id_images").addEventListener("change", function() {
    const files = this.files;
    const fileList = document.getElementById("file-list");
    fileList.innerHTML = "";

    if (files.length > 6) {
      alert("You can upload a maximum of 6 images.");
      this.value = "";
      return;
    }

    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const fileItem = document.createElement("div");
      fileItem.className = "file-item";

      if (file.type.match('image.*')) {
        const reader = new FileReader();
        reader.onload = function(e) {
          const img = document.createElement("img");
          img.src = e.target.result;
          img.width = 50;
          img.height = 50;
          img.style.objectFit = "cover";
          img.style.borderRadius = "4px";

          const span = document.createElement("span");
          span.className = "file-name";
          span.textContent = file.name;

          fileItem.appendChild(img);
          fileItem.appendChild(span);
        };
        reader.readAsDataURL(file);
      } else {
        const span = document.createElement("span");
        span.className = "file-name";
        span.textContent = file.name;
        fileItem.appendChild(span);
      }

      fileList.appendChild(fileItem);
    }
  });

  // Form validation before submission
  document.getElementById("ad-form").addEventListener("submit", function(e) {
    const files = document.getElementById("id_images").files;
    if (files.length > 6) {
      alert("Maximum 6 images allowed");
      e.preventDefault();
      return;
    }

    for (let i = 0; i < files.length; i++) {
      if (files[i].size > 5 * 1024 * 1024) {
        alert(`File "${files[i].name}" exceeds 5MB size limit`);
        e.preventDefault();
        return;
      }
    }
  });



     const form = document.getElementById("ad-form");
      const preview = {
        title: document.getElementById("title"),
        category: document.getElementById("category"),
        subcategory: document.getElementById("subcategory"),
        description: document.getElementById("description"),
        price: document.getElementById("price"),
        condition: document.getElementById("condition"),
        contact_phone: document.getElementById("contact_phone"),
        contact_email: document.getElementById("contact_email"),
        whatsapp_number: document.getElementById("whatsapp_number"),
        image_preview: document.getElementById("image-preview")
      };

      
      form.addEventListener("input", () => {
        const data = new FormData(form);
        preview.title.textContent = data.get("title") || '';
        preview.category.textContent = form.category.options[form.category.selectedIndex].text || '';
        preview.subcategory.textContent = form.subcategory.options[form.subcategory.selectedIndex].text || '';
        preview.description.textContent = data.get("description") || '';
        preview.price.textContent = data.get("price") ? ` $${data.get("price")}` : '';
        preview.condition.textContent = data.get("condition") ? ` ${data.get("condition")}` : '';
        preview.contact_phone.textContent = data.get("contact_phone") ? ` ${data.get("contact_phone")}` : '';
        preview.contact_email.textContent = data.get("contact_email") ? ` ${data.get("contact_email")}` : '';
        preview.whatsapp_number.textContent = data.get("whatsapp_number") ? ` ${data.get("whatsapp_number")}` : '';
      });

      form.images.addEventListener("change", () => {
        preview.image_preview.innerHTML = '';
        Array.from(form.images.files).forEach(file => {
          const reader = new FileReader();
          reader.onload = function(e) {
            const img = document.createElement('img');
            img.src = e.target.result;
            img.className = "preview";
            preview.image_preview.appendChild(img);
          };
          reader.readAsDataURL(file);
        });
      });
});

