// Бургер-меню, жанрлар тизмеси, корзина, избранное, реакциялар жана сатып алуу интерфейсинин иштөөсүнө жооп берет.
document.addEventListener("DOMContentLoaded", () => {
  const button = document.querySelector(".menu-btn");
  const menu = document.querySelector(".menu");
  if (button && menu) button.addEventListener("click", () => {
    const open = menu.classList.toggle("open");
    button.classList.toggle("active", open);
    button.setAttribute("aria-expanded", String(open));
  });

  menu?.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      menu.classList.remove("open");
      button?.classList.remove("active");
      button?.setAttribute("aria-expanded", "false");
    });
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      menu?.classList.remove("open");
      button?.classList.remove("active");
      button?.setAttribute("aria-expanded", "false");
      document.querySelector(".cart-drawer")?.classList.remove("open");
      document.querySelector(".cart-overlay")?.classList.remove("open");
      document.body.classList.remove("cart-is-open");
    }
  });

  const genreToggle = document.querySelector(".genre-menu-toggle");
  const genreDropdown = document.querySelector(".genre-dropdown");
  if (genreToggle && genreDropdown) {
    genreToggle.addEventListener("click", () => {
      const open = genreDropdown.classList.toggle("open");
      genreToggle.classList.toggle("active", open);
      genreToggle.setAttribute("aria-expanded", String(open));
    });
  }

  document.querySelectorAll(".genre-field select[multiple]").forEach((select) => {
    const picker = document.createElement("div");
    picker.className = "genre-picker";

    Array.from(select.options).forEach((option) => {
      const chip = document.createElement("button");
      chip.type = "button";
      chip.className = "genre-choice";
      chip.textContent = option.text;
      chip.classList.toggle("selected", option.selected);
      chip.setAttribute("aria-pressed", String(option.selected));
      chip.addEventListener("click", () => {
        option.selected = !option.selected;
        chip.classList.toggle("selected", option.selected);
        chip.setAttribute("aria-pressed", String(option.selected));
        select.dispatchEvent(new Event("change", { bubbles: true }));
      });
      picker.appendChild(chip);
    });

    select.classList.add("genre-native-select");
    select.insertAdjacentElement("afterend", picker);
  });

  const header = document.querySelector(".header");
  let ticking = false;

  const updateHeader = () => {
    const currentScrollY = window.scrollY;

    if (header) {
      if (currentScrollY > 2) {
        header.classList.add("header-hidden");
        menu?.classList.remove("open");
        button?.classList.remove("active");
        button?.setAttribute("aria-expanded", "false");
        genreDropdown?.classList.remove("open");
        genreToggle?.classList.remove("active");
        genreToggle?.setAttribute("aria-expanded", "false");
      } else {
        header.classList.remove("header-hidden");
      }
    }

    ticking = false;
  };

  window.addEventListener("scroll", () => {
    if (!ticking) {
      window.requestAnimationFrame(updateHeader);
      ticking = true;
    }
  }, { passive: true });

  const readStore = (key) => {
    try { return JSON.parse(localStorage.getItem(key)) || {}; }
    catch { return {}; }
  };
  const writeStore = (key, value) => localStorage.setItem(key, JSON.stringify(value));
  const catalogVersion = "requested-books-20260726";
  if (localStorage.getItem("book-catalog-version") !== catalogVersion) {
    ["bookshop-favorites", "bookshop-reactions", "bookshop-cart"].forEach((key) => {
      const stored = readStore(key);
      Object.keys(stored).forEach((id) => {
        if (id.startsWith("book-")) delete stored[id];
      });
      writeStore(key, stored);
    });
    localStorage.setItem("book-catalog-version", catalogVersion);
  }
  const cart = readStore("bookshop-cart");
  const favorites = readStore("bookshop-favorites");
  const reactions = readStore("bookshop-reactions");
  const cartDrawer = document.querySelector(".cart-drawer");
  const cartOverlay = document.querySelector(".cart-overlay");
  const cartList = document.querySelector("#cart-drawer-list");

  const closeCart = () => {
    cartDrawer?.classList.remove("open");
    cartOverlay?.classList.remove("open");
    cartDrawer?.setAttribute("aria-hidden", "true");
    document.body.classList.remove("cart-is-open");
  };

  const openCart = () => {
    renderCart();
    cartDrawer?.classList.add("open");
    cartOverlay?.classList.add("open");
    cartDrawer?.setAttribute("aria-hidden", "false");
    document.body.classList.add("cart-is-open");
  };

  const renderCart = () => {
    if (!cartList) return;
    const selectedBooks = { ...cart };
    const entries = Object.entries(selectedBooks);
    const drawerCount = document.querySelector("#drawer-items-count");
    const drawerTotal = document.querySelector("#drawer-total");
    const checkoutTotal = document.querySelector("#checkout-total");
    const itemCount = entries.reduce((sum, [, storedItem]) => {
      const quantity = Math.max(1, Number.parseInt(storedItem?.quantity || 1, 10));
      return sum + quantity;
    }, 0);
    const total = entries.reduce((sum, [, storedItem]) => {
      const value = Number.parseFloat(String(storedItem?.price || "0").replace(",", "."));
      const quantity = Math.max(1, Number.parseInt(storedItem?.quantity || 1, 10));
      return sum + (Number.isFinite(value) ? value * quantity : 0);
    }, 0);
    if (drawerCount) drawerCount.textContent = itemCount;
    if (drawerTotal) drawerTotal.textContent = total.toFixed(2);
    if (checkoutTotal) checkoutTotal.textContent = total.toFixed(2);
    if (!entries.length) {
      cartList.innerHTML = '<div class="cart-empty"><b>Корзина пока пуста</b><p>Добавьте понравившиеся книги из магазина.</p></div>';
      return;
    }
    cartList.innerHTML = entries.map(([id, storedItem]) => {
      const item = storedItem && typeof storedItem === "object" ? storedItem : {};
      const quantity = Math.max(1, Number.parseInt(item.quantity || 1, 10));
      return `
      <article class="cart-drawer-item">
        <span class="cart-book-mark">Ч</span>
        <div class="cart-item-info">
          <a href="${item.url || "#"}">${item.title || "Книга"}</a>
          ${item.price ? `<small>${item.price} сом</small>` : ""}
          <div class="cart-quantity" aria-label="Количество книги">
            <button type="button" data-cart-decrease="${id}" aria-label="Уменьшить количество">−</button>
            <b>${quantity}</b>
            <button type="button" data-cart-increase="${id}" aria-label="Увеличить количество">+</button>
          </div>
        </div>
        <button class="cart-remove" type="button" data-remove-cart="${id}" aria-label="Удалить ${item.title || "книгу"}">Удалить</button>
      </article>
    `;
    }).join("");
  };

  document.querySelectorAll(".cart-open").forEach((trigger) => {
    trigger.addEventListener("click", (event) => {
      event.preventDefault();
      openCart();
    });
  });

  document.querySelectorAll("[data-cart-close]").forEach((trigger) => {
    trigger.addEventListener("click", closeCart);
  });

  cartList?.addEventListener("click", (event) => {
    const increaseButton = event.target.closest("[data-cart-increase]");
    const decreaseButton = event.target.closest("[data-cart-decrease]");
    if (increaseButton || decreaseButton) {
      const id = (increaseButton || decreaseButton).dataset.cartIncrease ||
                 (increaseButton || decreaseButton).dataset.cartDecrease;
      if (!cart[id]) return;
      const current = Math.max(1, Number.parseInt(cart[id].quantity || 1, 10));
      cart[id].quantity = increaseButton ? current + 1 : Math.max(1, current - 1);
      writeStore("bookshop-cart", cart);
      refreshCounters();
      renderCart();
      return;
    }
    const removeButton = event.target.closest("[data-remove-cart]");
    if (!removeButton) return;
    const id = removeButton.dataset.removeCart;
    delete cart[id];
    delete favorites[id];
    writeStore("bookshop-cart", cart);
    writeStore("bookshop-favorites", favorites);
    document.querySelectorAll(`[data-cart-id="${id}"]`).forEach((button) => {
      button.classList.remove("active");
      button.textContent = "В корзину";
    });
    document.querySelectorAll(`[data-favorite-id="${id}"]`).forEach((button) => {
      button.classList.remove("active");
    });
    refreshCounters();
    renderCart();
  });

  const refreshCounters = () => {
    const cartTotal = Object.values(cart).reduce((sum, item) => {
      return sum + Math.max(1, Number.parseInt(item?.quantity || 1, 10));
    }, 0);
    const favoriteTotal = Object.keys(favorites).length;
    const cartCount = document.querySelector("#cart-count");
    const favoriteCount = document.querySelector("#favorite-count");
    if (cartCount) cartCount.textContent = cartTotal;
    if (favoriteCount) favoriteCount.textContent = favoriteTotal;
    document.querySelectorAll(".cart-count-copy").forEach((el) => el.textContent = cartTotal);
    document.querySelectorAll(".favorite-count-copy").forEach((el) => el.textContent = favoriteTotal);
  };

  document.querySelectorAll(".cart-btn").forEach((button) => {
    const id = button.dataset.cartId;
    if (cart[id]) {
      button.classList.add("active");
      button.textContent = "В корзине";
    }
    button.addEventListener("click", () => {
      if (cart[id]) {
        delete cart[id];
        button.classList.remove("active");
        button.textContent = "В корзину";
      } else {
        cart[id] = {
          title: button.dataset.title || id,
          price: button.dataset.price || "",
          url: button.dataset.url || "",
          quantity: 1
        };
        button.classList.add("active");
        button.textContent = "В корзине";
      }
      writeStore("bookshop-cart", cart);
      refreshCounters();
      if (cartDrawer?.classList.contains("open")) renderCart();
    });
  });

  document.querySelectorAll("[data-buy-now]").forEach((button) => {
    button.addEventListener("click", () => {
      const id = button.dataset.cartId;
      cart[id] = {
        title: button.dataset.title || id,
        price: button.dataset.price || "",
        url: button.dataset.url || "",
        quantity: Math.max(1, Number.parseInt(cart[id]?.quantity || 0, 10) + 1)
      };
      writeStore("bookshop-cart", cart);
      document.querySelectorAll(`[data-cart-id="${id}"].cart-btn`).forEach((cartButton) => {
        cartButton.classList.add("active");
        cartButton.textContent = "В корзине";
      });
      refreshCounters();
      openCart();
    });
  });

  const checkoutModal = document.querySelector("#checkout-modal");
  const checkoutForm = document.querySelector("#checkout-form");
  const checkoutSuccess = document.querySelector(".checkout-success");
  const openCheckout = () => {
    if (!Object.keys(cart).length) {
      openCart();
      return;
    }
    closeCart();
    renderCart();
    checkoutModal?.classList.add("open");
    checkoutModal?.setAttribute("aria-hidden", "false");
    document.body.classList.add("checkout-is-open");
  };
  const closeCheckout = () => {
    checkoutModal?.classList.remove("open");
    checkoutModal?.setAttribute("aria-hidden", "true");
    document.body.classList.remove("checkout-is-open");
  };

  document.querySelectorAll("[data-checkout-open]").forEach((button) => {
    button.addEventListener("click", openCheckout);
  });
  document.querySelectorAll("[data-checkout-close]").forEach((button) => {
    button.addEventListener("click", closeCheckout);
  });
  checkoutForm?.addEventListener("submit", (event) => {
    event.preventDefault();
    checkoutForm.hidden = true;
    checkoutSuccess.hidden = false;
    Object.keys(cart).forEach((id) => delete cart[id]);
    writeStore("bookshop-cart", cart);
    refreshCounters();
    renderCart();
  });

  document.querySelectorAll(".favorite-btn").forEach((button) => {
    const id = button.dataset.favoriteId;
    if (favorites[id]) button.classList.add("active");
    button.addEventListener("click", () => {
      if (favorites[id]) delete favorites[id];
      else {
        favorites[id] = {
          title: button.dataset.title || "Книга",
          price: button.dataset.price || "",
          url: button.dataset.url || ""
        };
      }
      button.classList.toggle("active", Boolean(favorites[id]));
      writeStore("bookshop-favorites", favorites);
      refreshCounters();
      if (cartDrawer?.classList.contains("open")) renderCart();
    });
  });

  const favoritesGrid = document.querySelector("#favorites-grid");
  const favoritesEmpty = document.querySelector("#favorites-empty");
  const favoritesPageCount = document.querySelector("#favorites-page-count");
  const escapeHtml = (value) => String(value || "").replace(/[&<>"']/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;"
  }[character]));

  const renderFavoritesPage = () => {
    if (!favoritesGrid) return;
    const entries = Object.entries(favorites).filter(([id]) => id.startsWith("book-"));
    if (favoritesPageCount) favoritesPageCount.textContent = entries.length;
    favoritesEmpty?.toggleAttribute("hidden", entries.length > 0);
    favoritesGrid.hidden = entries.length === 0;
    favoritesGrid.innerHTML = entries.map(([id, storedItem]) => {
      const item = storedItem && typeof storedItem === "object" ? storedItem : {};
      const title = escapeHtml(item.title || "Книга");
      const url = escapeHtml(item.url || "#");
      return `
        <article class="saved-book-card">
          <a class="saved-book-cover" href="${url}" aria-label="Открыть ${title}">
            <span>${escapeHtml((item.title || "К").slice(0, 1).toUpperCase())}</span>
            <small>Чилистен</small>
          </a>
          <div class="saved-book-info">
            <span class="saved-label">Избранная книга</span>
            <h3><a href="${url}">${title}</a></h3>
            <div>
              <a class="saved-open" href="${url}">Подробнее →</a>
              <button type="button" data-remove-favorite="${escapeHtml(id)}">Удалить</button>
            </div>
          </div>
        </article>
      `;
    }).join("");
  };

  favoritesGrid?.addEventListener("click", (event) => {
    const removeButton = event.target.closest("[data-remove-favorite]");
    if (!removeButton) return;
    delete favorites[removeButton.dataset.removeFavorite];
    writeStore("bookshop-favorites", favorites);
    refreshCounters();
    renderFavoritesPage();
  });

  renderFavoritesPage();

  document.querySelectorAll(".reaction-btn").forEach((button) => {
    const id = button.dataset.reactionId;
    const type = button.dataset.reaction;
    if (reactions[id] === type) button.classList.add("active");
    button.addEventListener("click", () => {
      reactions[id] = reactions[id] === type ? null : type;
      if (!reactions[id]) delete reactions[id];
      writeStore("bookshop-reactions", reactions);
      document.querySelectorAll(`[data-reaction-id="${id}"]`).forEach((item) => {
        item.classList.toggle("active", item.dataset.reaction === reactions[id]);
      });
    });
  });

  refreshCounters();

  document.querySelectorAll(".messages p").forEach((item) => {
    setTimeout(() => item.classList.add("hide"), 4500);
  });
});
