// Serves the Hugo-built static site, plus Markdown content negotiation for agents.
// Requests with `Accept: text/markdown` get the Markdown copy Hugo writes next to
// each page (index.md), or a Markdown 404 if there isn't one.

const MARKDOWN = "text/markdown; charset=utf-8";

function wantsMarkdown(request) {
  return /\btext\/markdown\b/i.test(request.headers.get("Accept") || "");
}

// Map a page URL path to its Markdown asset path, or null for non-page assets.
function markdownPath(pathname) {
  if (pathname.endsWith("/")) return pathname + "index.md";
  if (pathname.endsWith(".md")) return pathname;
  const last = pathname.slice(pathname.lastIndexOf("/") + 1);
  if (last.includes(".")) return null; // images, css, xml, txt, ...
  return pathname + "/index.md";
}

function withVary(response) {
  const res = new Response(response.body, response);
  res.headers.append("Vary", "Accept");
  return res;
}

function markdownNotFound(url) {
  const origin = url.origin;
  const body = `# 404: Page not found

There is no page at \`${url.pathname}\` on Kelvin Ma's blog.

Try one of these instead:

- [Home](${origin}/)
- [All posts](${origin}/posts/)
- [llms.txt: site summary and post list](${origin}/llms.txt)
- [Sitemap](${origin}/sitemap.xml)
`;
  return new Response(body, {
    status: 404,
    headers: { "Content-Type": MARKDOWN, Vary: "Accept" },
  });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const isRead = request.method === "GET" || request.method === "HEAD";

    if (isRead && wantsMarkdown(request)) {
      const mdPath = markdownPath(url.pathname);
      if (mdPath) {
        const mdUrl = new URL(mdPath, url.origin);
        const res = await env.ASSETS.fetch(new Request(mdUrl, request));
        if (res.status === 200 || res.status === 304) {
          const out = new Response(res.body, res);
          out.headers.set("Content-Type", MARKDOWN);
          out.headers.set("Vary", "Accept");
          return out;
        }
        return markdownNotFound(url);
      }
    }

    const res = await env.ASSETS.fetch(request);
    const type = res.headers.get("Content-Type") || "";
    return type.includes("text/html") ? withVary(res) : res;
  },
};
