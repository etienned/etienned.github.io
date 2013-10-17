#! /usr/bin/env python

import subprocess
import sys



def run(args):
    """
    Simplified subprocess runner. Check also return code and stderr and exit 
    on problems.
    """
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return_code = process.poll()
    if return_code != 0 or stderr:
        command = ' '.join(args)
        print """Problem running `%s`.
Return code: %s
STDOUT: ___________________
%s
STDERR: ___________________
%s
""" % (command, return_code, stdout, stderr)
        sys.exit(1)

    return stdout

def deploy():
    """
    Deploy Blog to Github account
    """
    # Check that everything is commited
    stdout = run(['git', 'status', '-s'])

    if stdout != '':
        print "Git status is not clean. Commit changes before deployment."
        print stdout
        sys.exit(1)

    # Build the blog to be sure everything is up to date
    print run(['nikola', 'build'])


    # Check that there's changes to commit
    stdout = run(['git', 'status', '-s'])
    if stdout != '':
        # Check if local is ahead of remote
        stdout = run(['git', 'rev-list', 'origin/master..HEAD'])
        # Add updated build files
        print run(['git', 'add', '-A', '..'])
        if stdout == '':
            # local is not ahead of remote so do a new commit
            print run(['git', 'commit', '-m', '"Rebuild site before deployment."'])
        else:
            # local is ahead so put changes made by the build in previous commit
            print run(['git', 'commit', '--amend', '-C', 'HEAD'])

    # Push repo to origin
    print run(['git', 'push', '--porcelain', 'origin', 'master'])



if __name__ == '__main__':
    deploy()