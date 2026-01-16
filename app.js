async function run() {
    const repo = document.getElementById("repo").value;
    const out = document.getElementById("out");
  
    out.textContent = "Processing...";
  
    const res = await fetch(
      "https://your-backend.onrender.com/analyze?repo_url=" +
      encodeURIComponent(repo)
    );
  
    out.textContent = JSON.stringify(await res.json(), null, 2);
  }