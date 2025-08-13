// รับอ้างอิงไปยังปุ่ม Options
const menuButton = document.getElementById('menu-button');

// รับอ้างอิงไปยังเมนู dropdown
const dropdownMenu = document.querySelector('.absolute');

// ซ่อนเมนู dropdown ในตอนเริ่มต้น
dropdownMenu.style.display = 'none';

// เพิ่ม Event Listener เมื่อคลิกที่ปุ่ม Options
menuButton.addEventListener('click', function() {
  // สลับการแสดงของเมนู dropdown
  if (dropdownMenu.style.display === 'none') {
    dropdownMenu.style.display = 'block';
  } else {
    dropdownMenu.style.display = 'none';
  }
});
