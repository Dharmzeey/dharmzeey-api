"""One-off seed: import the "B2 + Cloudflare custom media domain" post.

Run:  python seed_blog_b2_cloudflare.py
Safe to re-run — uses update_or_create keyed on slug.
"""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.dev")
django.setup()

from django.utils import timezone  # noqa: E402

from blog.models import BlogPost, Tag  # noqa: E402

TITLE = "How to Serve Media Files via a Custom Subdomain Using Backblaze B2 and Cloudflare"
SLUG = "serve-media-custom-subdomain-backblaze-b2-cloudflare"

EXCERPT = (
    "Raw storage URLs like f003.backblazeb2.com/file/bucket/image.jpg look "
    "unprofessional and leak your storage provider. Here's how to serve files "
    "from media.yourdomain.com instead, using Backblaze B2 and Cloudflare — "
    "with free bandwidth between them, CDN caching, and the one URL rewrite "
    "rule most guides skip."
)

META_TITLE = "Serve Media via a Custom Subdomain with Backblaze B2 + Cloudflare"
META_DESCRIPTION = (
    "Step-by-step guide to serving Backblaze B2 files from your own subdomain "
    "with Cloudflare: CNAME setup, the critical URL rewrite rule, and Django "
    "and Next.js config."
)

TAGS = ["Backblaze B2", "Cloudflare", "DevOps", "Django", "CDN"]

READ_TIME_MINUTES = 6

CONTENT = """\
<p>If you store media files in an object storage service like Backblaze B2, the last thing you want is exposing a raw storage URL like <code>f003.backblazeb2.com/file/your-bucket/image.jpg</code> to your users. It looks unprofessional, leaks your storage provider, and gives you zero control over caching or routing.</p>

<p>In this guide you'll learn how to serve your files through a clean branded subdomain &mdash; something like <code>media.yourdomain.com</code> &mdash; using Backblaze B2 as the storage backend and Cloudflare to handle DNS, CDN caching, and URL rewriting.</p>

<p>The best part: <strong>Backblaze and Cloudflare are bandwidth alliance partners</strong>, which means traffic between them is free. You only pay for storage, not egress.</p>

<h2>What You Need</h2>

<ul>
  <li>A <strong>Backblaze B2</strong> account</li>
  <li>A <strong>domain name</strong> (registered anywhere)</li>
  <li>A <strong>Cloudflare account</strong> (free tier is enough)</li>
</ul>

<p>If your domain is not registered on Cloudflare, don't worry &mdash; there are two ways to handle that, covered at the end of this guide.</p>

<h2>Step 1: Create a Public Bucket on Backblaze B2</h2>

<p>Log into Backblaze B2 and create a new bucket.</p>

<ul>
  <li>Set the bucket to <strong>Public</strong></li>
  <li>Note your bucket name &mdash; you'll need it for the rewrite rule</li>
  <li>Note your endpoint URL &mdash; it looks like <code>f003.backblazeb2.com</code></li>
</ul>

<blockquote>
  <p>The <code>f003</code> part varies by account. Check your bucket details to confirm yours.</p>
</blockquote>

<p>Once your bucket is created, upload a test file so you can verify the setup end to end.</p>

<h2>Step 2: Add a CNAME Record in Cloudflare</h2>

<p>In your Cloudflare dashboard, go to <strong>DNS &rarr; Records &rarr; Add record</strong>.</p>

<table>
  <thead>
    <tr>
      <th>Field</th>
      <th>Value</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Type</td><td>CNAME</td></tr>
    <tr><td>Name</td><td><code>media</code></td></tr>
    <tr><td>Target</td><td><code>f003.backblazeb2.com</code></td></tr>
    <tr><td>Proxy</td><td>Enabled (orange cloud on)</td></tr>
    <tr><td>TTL</td><td>Auto</td></tr>
  </tbody>
</table>

<p>Click <strong>Save</strong>.</p>

<p>This creates <code>media.yourdomain.com</code> as a proxied alias to your Backblaze endpoint. Cloudflare sits in between &mdash; handling caching, HTTPS, and routing.</p>

<h2>Step 3: Add a URL Rewrite Rule (Critical)</h2>

<p>This step is the one most guides skip &mdash; and it's the most important one.</p>

<p>Without a rewrite rule, your subdomain points to the root of the Backblaze endpoint, not your specific bucket. That means anyone could theoretically use your domain to serve files from <em>any</em> Backblaze bucket. The rewrite rule locks requests to your bucket's path.</p>

<p>In Cloudflare, go to <strong>Rules &rarr; Transform Rules &rarr; URL Rewrite &rarr; Create rule</strong>.</p>

<p>Configure it as follows:</p>

<p><strong>When incoming requests match:</strong></p>

<pre><code>Hostname equals media.yourdomain.com
</code></pre>

<p><strong>Then rewrite the path &mdash; Rewrite to (Dynamic):</strong></p>

<pre><code>concat("/file/your-bucket-name", http.request.uri.path)
</code></pre>

<p>Replace <code>your-bucket-name</code> with the actual name of your Backblaze bucket.</p>

<p><strong>What this does:</strong> A request to <code>media.yourdomain.com/product/iphone-14.jpg</code> gets rewritten internally to <code>/file/your-bucket-name/product/iphone-14.jpg</code> before Backblaze receives it. Your users never see the bucket path.</p>

<h2>Step 4: Verify It Works</h2>

<p>Once DNS propagates (usually within a few minutes on Cloudflare), test by visiting:</p>

<pre><code>https://media.yourdomain.com/your-test-file.jpg
</code></pre>

<p>You can also verify DNS resolution from the command line:</p>

<pre><code class="language-bash">nslookup media.yourdomain.com 1.1.1.1
</code></pre>

<p>If it returns an IP address, the record is live. If you get <code>Non-existent domain</code>, the record hasn't saved correctly &mdash; go back and check Step 2.</p>

<h2>Step 5: Configure Your Backend to Use the Custom Domain</h2>

<p>Your backend is probably still generating URLs pointing to the raw Backblaze endpoint. Update it to use your new subdomain.</p>

<p><strong>Django (<code>settings.py</code>):</strong></p>

<pre><code class="language-python"># Before
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_ENDPOINT_URL = 'https://s3.us-west-004.backblazeb2.com'
AWS_S3_CUSTOM_DOMAIN = 'f003.backblazeb2.com'

# After
AWS_S3_CUSTOM_DOMAIN = 'media.yourdomain.com'
MEDIA_URL = 'https://media.yourdomain.com/'
</code></pre>

<p><strong>Next.js (<code>next.config.js</code>) &mdash; allow the domain for image optimization:</strong></p>

<pre><code class="language-js">module.exports = {
  images: {
    domains: ['media.yourdomain.com'],
  },
}
</code></pre>

<p><strong>Environment variable approach:</strong></p>

<pre><code class="language-env">MEDIA_BASE_URL=https://media.yourdomain.com
</code></pre>

<p>Then reference it anywhere you build file URLs:</p>

<pre><code class="language-python"># Python example
image_url = f"{settings.MEDIA_URL}{instance.image.name}"
</code></pre>

<p>From this point, every media file your app references will be served through Cloudflare &mdash; with CDN caching on top at no extra bandwidth cost.</p>

<h2>What If Your Domain Is Not on Cloudflare?</h2>

<p>You have two options depending on what your domain provider supports.</p>

<h3>Option A: Add the CNAME at Your Domain Provider (No Migration)</h3>

<p>If your domain provider supports CNAME records and URL rewrite rules, you can add the CNAME there directly without touching Cloudflare:</p>

<pre><code>Type:  CNAME
Name:  media
Value: f003.backblazeb2.com
</code></pre>

<p>The limitation here is that most shared hosting providers (cPanel, Asura, etc.) don't offer Cloudflare-style URL rewrite rules. Without the rewrite rule from Step 3, your subdomain will point to the Backblaze root, not your specific bucket &mdash; which is a security and routing issue.</p>

<p>If your provider supports it, great. If not, use Option B.</p>

<h3>Option B: Migrate Your DNS to Cloudflare (Recommended)</h3>

<p>This is easier than it sounds. You're not moving your hosting &mdash; just changing where DNS is managed.</p>

<ol>
  <li>Create a free Cloudflare account and add your domain</li>
  <li>Cloudflare will scan and import your existing DNS records automatically</li>
  <li>Verify all records imported correctly (A records, MX for email, existing CNAMEs)</li>
  <li>Go to your domain registrar and update the nameservers to the ones Cloudflare provides:</li>
</ol>

<pre><code>e.g.
aria.ns.cloudflare.com
bob.ns.cloudflare.com
</code></pre>

<ol start="5">
  <li>Wait for propagation &mdash; typically <strong>30 minutes to 24 hours</strong></li>
  <li>Once propagated, follow Steps 2 and 3 above in your Cloudflare dashboard</li>
</ol>

<p>Your hosting, VPS, SSL certs, and everything else stays exactly where it is. Only DNS management moves to Cloudflare.</p>

<h2>Summary</h2>

<table>
  <thead>
    <tr>
      <th>Step</th>
      <th>What You Do</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>1</td><td>Create a public Backblaze B2 bucket</td></tr>
    <tr><td>2</td><td>Add a proxied CNAME in Cloudflare DNS</td></tr>
    <tr><td>3</td><td>Add a URL rewrite rule scoped to your bucket path</td></tr>
    <tr><td>4</td><td>Verify DNS resolution and file serving</td></tr>
    <tr><td>5</td><td>Update your backend to use the custom domain</td></tr>
  </tbody>
</table>

<p>You now have a clean branded media URL, free bandwidth between Cloudflare and Backblaze, CDN edge caching globally, and full control over how your files are served &mdash; without exposing your storage provider or paying egress fees.</p>
"""


def run():
    post, created = BlogPost.objects.update_or_create(
        slug=SLUG,
        defaults={
            "title": TITLE,
            "content": CONTENT,
            "excerpt": EXCERPT,
            "meta_title": META_TITLE,
            "meta_description": META_DESCRIPTION,
            "read_time_minutes": READ_TIME_MINUTES,
            "published_date": timezone.now(),
            "is_published": True,
        },
    )
    tags = []
    for name in TAGS:
        tag, _ = Tag.objects.get_or_create(name=name)
        tags.append(tag)
    post.tags.set(tags)
    print(f"{'Created' if created else 'Updated'} post: {post.title} ({post.slug})")


if __name__ == "__main__":
    run()
