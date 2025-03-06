## How UV Works

### Use Case

The main case for including a `UV` option in `catkin_virtualenv` is for hosts where a large number of virtual environments are created and those virtual environments share a sizeable number of identical packages. 

`UV` benefits this use case by deduplicating packages installed into each virtual environment

### How it works
The deduplication feature of UV works by creating a single shared hardlink farm, we will call this the `cache`.  Each time we attempt to install a pip package into a `venv` the following is performed

1. `UV` checks if the package is available in the `cache`
2. If the package is not available then the package is downloaded and placed in the `cache`
3. The package is available in the `cache` at this point.
4. Instead of copying the package from the `cache` into the `venv` the package is hardlinked into the `venv`
5. Because packages are hardlinked there a no issues one might find with symlinks. They are identical to files created by installing directly into the `venv`

##### Hardlinking

```
Every file on the Linux filesystem starts with a single hard link. The link is between the filename and the actual data stored on the filesystem. Creating an additional hard link to a file means a few different things.

When changes are made to one filename, the other reflects those changes. The permissions, link count, ownership, timestamps, and file content are the exact same. If the original file is deleted, the data still exists under the secondary hard link. The data is only removed from your drive when all links to the data have been removed. If you find two files with identical properties but are unsure if they are hard-linked, use the ls -i command to view the inode number. Files that are hard-linked together share the same inode number.

```

Ref : [Red Hat Hardlinks](https://www.redhat.com/sysadmin/linking-linux-explained)

### How do I use it

Use of `UV` is currently opt-in. 
To use it modify your `catkin_generate_virtualenv` to resemble the following

```
catkin_generate_virtualenv(
  INPUT_REQUIREMENTS requirements.in
  USE_UV TRUE
  UV_CACHE /tmp/testing/uv/cache
)

```

#### Configuration

 #TODO Document OPTIONS

 `UV` aims to be identical in usage to`Pip`, however there are configration differences. We do not allow mixing of `PIP` arguments with `UV` arguments. 

**Allowed**
 ```
 catkin_generate_virtualenv(
  INPUT_REQUIREMENTS requirements.in
  USE_UV TRUE
  UV_CACHE /tmp/testing/uv/cache
  EXTRA_UV_ARGS ....
)
 
 ```

**Not Allowed**
```
 catkin_generate_virtualenv(
  INPUT_REQUIREMENTS requirements.in
  USE_UV TRUE
  UV_CACHE /tmp/testing/uv/cache
  EXTRA_PIP_ARGS ....
)

```