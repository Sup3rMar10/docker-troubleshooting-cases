# docker-troubleshooting-cases

> **Reference only.** Five common container problems, each with a "broken" and a "fixed" version and the reasoning. The cases were **not executed** here: the symptoms and fixes are written from experience and standard Docker behaviour, and the exact error text can differ by Docker version. The only tool run was `docker build --check` (Docker's linter) on the Dockerfiles: it flagged case 1's broken file with `JSONArgsRecommended` (shell-form `CMD`), which matches the diagnosis, and reported no warnings on the others (it does not detect the other problems).

For each case: symptom, how to confirm the cause, fix.

| # | Symptom | Cause | Fix |
|---|---|---|---|
| 1 | `docker stop` takes 10 seconds; the app never shuts down cleanly | Shell-form `CMD`: a shell is PID 1 and does not forward SIGTERM | Exec form `CMD ["..."]`, or `init: true` / `--init`; handle SIGTERM in the app |
| 2 | `Permission denied` writing to a mounted volume | Container runs as non-root; the volume is owned by root | `chown` in the image, `--user` matching the host, or `fsGroup` on Kubernetes |
| 3 | Container is "unhealthy" though the app works | Healthcheck uses `curl`, which the slim image does not have | Use a tool in the image (Python one-liner), or install curl deliberately |
| 4 | `connection refused` to another container | Used `localhost`, or containers are on different networks | Use the service name on a shared user-defined network |
| 5 | `exec ./entrypoint.sh: no such file or directory` (the file is there) | Script has Windows CRLF line endings; the shebang becomes `bash\r` | LF endings, enforced with `.gitattributes` (`*.sh text eol=lf`) |

Case 5 is the classic Windows-to-Linux trap and the least obvious error message of the five.

## Layout

```
cases/01-signals/       Dockerfile.broken  Dockerfile.fixed
cases/02-volume-permissions/  Dockerfile.broken  Dockerfile.fixed
cases/03-healthcheck/   Dockerfile.broken  Dockerfile.fixed
cases/04-networking/    compose.broken.yaml  compose.fixed.yaml
cases/05-crlf/          Dockerfile  entrypoint.sh  .gitattributes
```

## First commands for any broken container

```
docker ps -a                       # is it running, restarting, exited? exit code?
docker logs --tail 100 <name>
docker inspect <name> --format '{{.State.ExitCode}} {{.State.Health.Status}}'
docker exec -it <name> sh          # look around (if it stays up)
docker run --rm -it --entrypoint sh <image>   # if it will not stay up
```

Exit code 137 usually means killed (out of memory or SIGKILL after a stop timeout); 143 is SIGTERM; 126 and 127 are "cannot execute" and "not found".

## Not checked

None of the cases were run (beyond the lint above). Treat the commands as a checklist to verify, not as recorded output.

MIT licensed.
