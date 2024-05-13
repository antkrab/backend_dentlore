
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/Users/ant/opt/anaconda3/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/Users/ant/opt/anaconda3/etc/profile.d/conda.sh" ]; then
        . "/Users/ant/opt/anaconda3/etc/profile.d/conda.sh"
    else
        export PATH="/Users/ant/opt/anaconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
export PATH="$PATH:$HOME/flutter/bin"
export JAVA_HOME="/Applications/Android 
Studio.app/Contents/jre/jdk/Contents/Home"
export PATH="$HOME/.jenv/bin:$PATH"
eval "$(jenv init -)"
export PATH="$PATH:/Users/ant/.npm-packages/lib/vercel@34.1.7/bin
