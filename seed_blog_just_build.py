"""One-off seed: import the "Stop Waiting for Validation" post from Contentful.

Run:  python seed_blog_just_build.py
Safe to re-run — uses update_or_create keyed on slug.
"""
import os
from datetime import datetime, timezone as dt_timezone

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.dev")
django.setup()

from blog.models import BlogPost, Tag  # noqa: E402

TITLE = "Stop Waiting for Validation — Just Build"
SLUG = "stop-waiting-for-validation-just-build"

PUBLISHED_DATE = datetime(2025, 10, 14, 9, 0, tzinfo=dt_timezone.utc)

EXCERPT = (
    "Everyone says validate your idea before building. But if your idea solves "
    "a problem you actually have, that's already your first validation. Why "
    "waiting for surveys and perfect prototypes costs you momentum — and why "
    "shipping the working core early beats polishing in the dark."
)

META_TITLE = "Stop Waiting for Validation — Just Build"
META_DESCRIPTION = (
    "Idea validation is good, but execution is better. Why developers should "
    "build the core, ship early, and iterate instead of waiting for perfect "
    "validation."
)

TAGS = ["Career", "Indie Hacking", "Product", "Software Development"]

READ_TIME_MINUTES = 3

CONTENT = """\
<p>There's always that one developer out there, architecting the perfect backend.<br />
No users. No feedback.<br />
Just building what he thinks people want.</p>

<p>Don't be that developer.</p>

<p>Or maybe&hellip; <strong>do</strong> be that developer.</p>

<p>Many people will tell you that you must validate your idea before building.
But here's the thing &mdash; if your idea solves a real problem you face, that's already your first validation.
If it's useful to you, chances are someone else out there needs it too.</p>

<p>Now, surveys and forms sound like a great way to test an idea, right?
But let's be honest &mdash; can you really translate your solution into a few survey questions that capture the real essence of what you want to build?
Even if you can, how sure are you that your survey will reach the right people &mdash; the ones who truly feel the same pain point?</p>

<p>By waiting too long for perfect validation, you risk losing valuable time and momentum that could've gone into building, learning, and improving.</p>

<h2>⚙️ Be the Builder</h2>

<p>Sometimes, it's better to be that developer &mdash; the one who keeps building even without early applause.
Because as the saying goes:</p>

<blockquote>
  <p>&ldquo;The man who sleeps with a cutlass is a fool &mdash; until the day he catches a thief.&rdquo;</p>
</blockquote>

<p>If you don't have a job or a startup budget, build and design as many tough projects as you can.
Don't let the &ldquo;get-users-first&rdquo; narrative stop you from learning how big systems actually work under the hood.</p>

<h2>🚀 Ship Fast. Iterate Faster.</h2>

<p>When you start building, don't wait for the perfect prototype.
Don't wait for everything to look and feel flawless.
Build the core function &mdash; the version that works &mdash; and deploy it.</p>

<p>Organic growth takes time.
Unless you have a large following or money for marketing, your product won't hit user milestones overnight.
But if you start early and keep improving while sharing your journey, you'll gradually build both your product and your audience.</p>

<p>By the time your &ldquo;perfect&rdquo; version is ready, you might already have tens &mdash; maybe hundreds &mdash; of real users who believe in what you're building.</p>

<h2>🎯 Lesson</h2>

<p>Don't over-rely on idea validation before starting out.
Validation is good, but execution is better.
Build, learn, ship, and repeat &mdash; that's how real products and real builders grow.</p>
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
            "published_date": PUBLISHED_DATE,
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
