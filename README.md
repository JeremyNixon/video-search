# Video Search Engine - https://vibes.video

This is an implementation of a simple, lightweight neural dense vector search powered semantic video search engine.

The model uses CLIP embeddings and FAISS to take textual search queries and to navigate through similar video frames by clicking on them in a simple same-energy inspired interface.


## Installation:
```
git clone https://github.com/JeremyNixon/video-search.git
cd video-search
pip install -r requirements.txt
```

## Usage:
Add the images you'd like to index to the static/ folder.
Run the indexer.

```python3 process_data.py```

When indexing is complete, start the server:

```gunicorn app:app```

The webapp will be up and running at either localhost or at your server's IP address.


## Images

Play Button SVG Vector https://www.svgrepo.com/svg/13672/play-button
Search Globe SVG https://www.svgrepo.com/svg/522651/search-globe


## HowTo - install ssh certificates

Typical flow is
1. Follow certbot [installation instructions](https://certbot.eff.org/instructions) for your distro
1. Make sure nginx vhost.conf for domain you want to host has the server_name directive in it, set it up to proxy to the gunicorn server and host it on http i.e. port 80
1. Also make sure that the vhost.conf is at /etc/nginx/sites-available/vibes.video and symlinked to /etc/nginx/sites-enabled/vibes.video
1. `sudo certbot –nginx -d vibes.video` … it will prompt you for an email etc and handle the rest
1. Other useful commands are `sudo nginx -t` to check if the updated conf files compile and `sudo service nginx reload` which reloads nginx



