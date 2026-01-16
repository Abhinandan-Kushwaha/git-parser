async function run() {
    const repo = document.getElementById("repo").value;
    const out = document.getElementById("out");
  
    out.textContent = "Processing...";
  
    const res = await fetch(
      "https://git-parser.onrender.com/analyze?repo_url=https://github.com/Abhinandan-Kushwaha/git-parser" +
      encodeURIComponent(repo)
    );
  
    out.textContent = JSON.stringify(await res.json(), null, 2);
  }