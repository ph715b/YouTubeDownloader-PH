const { app, BrowserWindow, ipcMain } = require("electron");
const ytdl = require("ytdl-core");
const fs = require("fs");
const path = require("path");

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
    },
  });

  mainWindow.loadFile("src/index.html");
}

app.whenReady().then(() => {
  createWindow();

  app.on("activate", function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on("window-all-closed", function () {
  if (process.platform !== "darwin") app.quit();
});

ipcMain.on("download", (event, { url, location }) => {
  const youtubeStream = ytdl(url, { quality: "highest" });
  const savePath = path.join(location, "video.mp4");

  youtubeStream.pipe(fs.createWriteStream(savePath));

  youtubeStream.on("finish", () => {
    mainWindow.webContents.send("downloadCompleted");
  });

  youtubeStream.on("error", (error) => {
    mainWindow.webContents.send("downloadError", error.message);
  });
});
