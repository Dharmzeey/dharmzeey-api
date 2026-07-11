"""One-off seed: import the "Supabase backup" post from Contentful into Django.

Run:  python seed_blog_supabase_backup.py
Safe to re-run — uses update_or_create keyed on slug.
"""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.dev")
django.setup()

from django.utils import timezone  # noqa: E402

from blog.models import BlogPost, Tag  # noqa: E402

TITLE = "My Supabase Backups Were Failing Silently for Months — Here's How I Fixed Them"
SLUG = "supabase-backup-github-actions-backblaze-b2"

EXCERPT = (
    "My daily GitHub Actions job that dumps a Supabase Postgres database to "
    "Backblaze B2 had been failing silently for months. The culprits: a pg_dump "
    "version mismatch and Supabase's IPv6-only direct connection. Here's how I "
    "diagnosed both, plus the full working workflow YAML."
)

META_TITLE = "Fixing Silent Supabase Backup Failures in GitHub Actions"
META_DESCRIPTION = (
    "A pg_dump version mismatch and an IPv6 gotcha broke my daily Supabase "
    "backups for months. How I fixed both, with a working GitHub Actions to "
    "Backblaze B2 workflow."
)

TAGS = ["Supabase", "GitHub Actions", "PostgreSQL", "Backblaze B2", "DevOps"]

READ_TIME_MINUTES = 7

CONTENT = """\
<p>I have a project running on Supabase's free plan. It has been live for about four months &mdash; small app, but real data. Sales records, inventories, user entries. The kind of stuff that doesn't grow back if it disappears.</p>

<p>I've always believed one thing about software: the backend logic and the frontend logic can crash, and you can rebuild them. But the database must always be backed up, because once it goes, it's gone.</p>

<p>So I wrote a GitHub Actions YAML file to automatically dump my Supabase database every day and ship it to Backblaze B2 for storage. That was the plan. The problem? It had been failing silently for months.</p>

<p>Every single day: failed. Failed. Failed.</p>

<p>Until I decided to actually sit down and fix it.</p>

<h2>The Two Problems I Found</h2>

<h3>Issue 1 &mdash; PostgreSQL Version Mismatch</h3>

<p>The first issue was a PostgreSQL version mismatch.</p>

<p>Supabase runs PostgreSQL 17. But when GitHub Actions installs the PostgreSQL client by default, it pulls version 16. So <code>pg_dump</code> v16 was trying to connect to a v17 server &mdash; and it refused.</p>

<p>The fix was straightforward: explicitly install <code>postgresql-client-17</code> in the workflow instead of using the default.</p>

<pre><code class="language-yaml">- name: Install PostgreSQL client
  run: |
    sudo apt-get update
    sudo apt-get install -y gnupg curl

    curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc \\
      | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg

    echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" \\
      | sudo tee /etc/apt/sources.list.d/pgdg.list

    sudo apt-get update
    sudo apt-get install -y postgresql-client-17
</code></pre>

<h3>Issue 2 &mdash; IPv6 vs IPv4 (The Sneaky One)</h3>

<p>After fixing the version mismatch, there was another twist.</p>

<p>When you open your Supabase dashboard and grab the direct connection string, it uses IPv6 by default. But GitHub Actions runners only support IPv4. The result is a connection error that asks: <em>&ldquo;Is the server accepting TCP connections?&rdquo;</em> &mdash; which looks like a password problem but isn't. It's purely a networking configuration issue.</p>

<p>If you're on a Supabase paid plan, you can enable an IPv4 add-on directly. On the free plan, the workaround is to use the <strong>Transaction Pooler</strong> instead of the direct connection or the session pooler.</p>

<p>The changes:</p>

<table>
  <thead>
    <tr>
      <th>Setting</th>
      <th>Direct Connection</th>
      <th>Transaction Pooler</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Host</td>
      <td>Direct host</td>
      <td>Pooler host (different)</td>
    </tr>
    <tr>
      <td>Port</td>
      <td>5432</td>
      <td>6543</td>
    </tr>
    <tr>
      <td>Username</td>
      <td><code>postgres</code></td>
      <td><code>postgres.[project-id]</code></td>
    </tr>
  </tbody>
</table>

<p>The username must have your Supabase project ID appended to it. You'll find all of this under <strong>Project Settings &rarr; Database &rarr; Connection string &rarr; Transaction pooler</strong> in your Supabase dashboard.</p>

<h2>The Full Working YAML</h2>

<p>Once both issues were sorted, I stored all the connection values as GitHub Secrets and updated the workflow. I also switched from the AWS CLI to the Backblaze B2 CLI directly &mdash; simpler and no unnecessary dependencies.</p>

<pre><code class="language-yaml">name: Daily Supabase Backup to Backblaze B2

on:
  schedule:
    - cron: '0 2 * * *'  # Runs daily at 2:00 AM UTC. You can change this
  workflow_dispatch:       # Allows manual trigger (on the github)

jobs:
  backup:
    runs-on: ubuntu-latest

    steps:
      - name: Install PostgreSQL client
        run: |
          sudo apt-get update
          sudo apt-get install -y gnupg curl

          curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc \\
            | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg

          echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" \\
            | sudo tee /etc/apt/sources.list.d/pgdg.list

          sudo apt-get update
          sudo apt-get install -y postgresql-client-17

      - name: Dump Supabase database
        env:
          PGPASSWORD: ${{ secrets.SUPABASE_DB_PASSWORD }}
        run: |
          TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
          FILENAME="supabase_backup_${TIMESTAMP}.sql.gz"
          echo "FILENAME=$FILENAME" &gt;&gt; $GITHUB_ENV

          pg_dump \\
            --host=${{ secrets.SUPABASE_DB_HOST }} \\
            --port=${{ secrets.SUPABASE_DB_PORT }} \\
            --username=${{ secrets.SUPABASE_DB_USER }} \\
            --dbname=${{ secrets.SUPABASE_DB_NAME }} \\
            --no-owner \\
            --no-acl \\
            --format=plain \\
          | gzip &gt; "$FILENAME"

      - name: Install B2 CLI
        run: pip install b2

      - name: Upload to Backblaze B2
        env:
          B2_APPLICATION_KEY_ID: ${{ secrets.B2_APPLICATION_KEY_ID }}
          B2_APPLICATION_KEY: ${{ secrets.B2_APPLICATION_KEY }}
        run: |
          b2 authorize-account "$B2_APPLICATION_KEY_ID" "$B2_APPLICATION_KEY"
          b2 upload-file ${{ secrets.B2_BUCKET_NAME }} "$FILENAME" "backups/$FILENAME"

      - name: Clean up local dump file
        run: rm -f "$FILENAME"

      - name: Delete backups older than 30 days
        env:
          B2_APPLICATION_KEY_ID: ${{ secrets.B2_APPLICATION_KEY_ID }}
          B2_APPLICATION_KEY: ${{ secrets.B2_APPLICATION_KEY }}
        run: |
          b2 authorize-account "$B2_APPLICATION_KEY_ID" "$B2_APPLICATION_KEY"
          CUTOFF=$(date -d '30 days ago' +%s)000

          b2 ls --json ${{ secrets.B2_BUCKET_NAME }} backups/ | \\
          python3 -c "
          import sys, json
          files = json.load(sys.stdin)
          cutoff = $CUTOFF
          for f in files:
              if f['uploadTimestamp'] &lt; cutoff:
                  print(f['fileName'])
          " | while read fname; do
            b2 hide-file ${{ secrets.B2_BUCKET_NAME }} "$fname"
          done
</code></pre>

<h2>GitHub Secrets to Configure</h2>

<p>You'll need to add these secrets to your repository under <strong>Settings &rarr; Secrets and variables &rarr; Actions</strong>:</p>

<table>
  <thead>
    <tr>
      <th>Secret</th>
      <th>What it is</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>SUPABASE_DB_HOST</code></td>
      <td>Transaction pooler host from Supabase dashboard</td>
    </tr>
    <tr>
      <td><code>SUPABASE_DB_PORT</code></td>
      <td><code>6543</code> (transaction pooler port)</td>
    </tr>
    <tr>
      <td><code>SUPABASE_DB_USER</code></td>
      <td><code>postgres.[your-project-id]</code></td>
    </tr>
    <tr>
      <td><code>SUPABASE_DB_NAME</code></td>
      <td>Your database name (usually <code>postgres</code>)</td>
    </tr>
    <tr>
      <td><code>SUPABASE_DB_PASSWORD</code></td>
      <td>Your database password</td>
    </tr>
    <tr>
      <td><code>B2_APPLICATION_KEY_ID</code></td>
      <td>From Backblaze B2 app keys</td>
    </tr>
    <tr>
      <td><code>B2_APPLICATION_KEY</code></td>
      <td>From Backblaze B2 app keys</td>
    </tr>
    <tr>
      <td><code>B2_BUCKET_NAME</code></td>
      <td>Your Backblaze bucket name</td>
    </tr>
  </tbody>
</table>

<h2>The Result</h2>

<p>When I ran the workflow after fixing everything, it went through smoothly and error free this time. Initially, the backup file was always around 20 bytes, which is basically an empty dump (just the <code>pg_dump</code> header, no actual data). After the fix, the compressed backup came in at 383 KB.</p>

<p>I extracted it and opened it and my database has been backed up &mdash; the schema, the sales records. All of it. The beautiful thing is that it does it every single day without supervision. That was a good feeling.</p>

<h2>A Note on Object Storage</h2>

<p>I used Backblaze B2 because it's what I already use for my media and files. But this workflow works with any S3-compatible object storage &mdash; AWS S3, DigitalOcean Spaces, Cloudflare R2. The only thing you'd change is the CLI tool and its configuration. The <code>pg_dump</code> step and the GitHub Secrets pattern stay exactly the same.</p>
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
