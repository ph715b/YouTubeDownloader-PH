const { ipcRenderer } = require("electron");

const downloadBtn = document.getElementById("downloadBtn");

downloadBtn.addEventListener("click", () => {
  const url = document.getElementById("url").value;
  const location = document.getElementById("location").value;
  ipcRenderer.send("download", { url, location });
});
