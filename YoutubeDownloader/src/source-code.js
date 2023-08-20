const readline = require("readline");
const ytdl = require("ytdl-core");

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

function downloadVideo(link, savePath) {
  const youtubeStream = ytdl(link, { quality: "highest" });

  youtubeStream.pipe(fs.createWriteStream(savePath));

  youtubeStream.on("finish", () => {
    console.log("Download completed successfully");
    rl.close();
  });

  youtubeStream.on("error", (error) => {
    console.error("An error has occurred:", error);
    rl.close();
  });
}

function main() {
  rl.question("Enter the YouTube video URL: ", (link) => {
    rl.question("Enter the download location: ", (downloadLocation) => {
      downloadVideo(link, downloadLocation);
    });
  });
}

main();
