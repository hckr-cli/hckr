Shell Completion
=====================================
``hckr`` provides tab completion support for **Bash** (version 4.4 and up), **Zsh**.
After

.. hint::
    ``commands`` can be auto completed using double tab, for ``options`` insert '-' and then use tab.

    .. code-block::

        $ hckr <TAB><TAB>
            cron    -- cron commands
            crypto  -- crypto commands
            data    -- data related commands
            hash    -- hash commands
            info    -- info commands
            k8s     -- Kubernetes commands
            repl    -- Start an interactive shell.

        $ hckr hash md5 -<TAB><TAB>
            --chunk-size  -c  -- Size of chunks for file hash
            --file        -f  -- File to be hashed
            --help        -h  -- Show this message and exit.
            --string      -s  -- String to be hashed



Shell completion for Bash
-------------------------
If you are using **bash**, please run this in your terminal, this will enable shell completion

.. code-block::

    echo 'eval "$(_HCKR_COMPLETE=bash_source hckr)"' >> ~/.bashrc


Shell completion for Zshrc
--------------------------
If you are using **zsh**, please run this in your terminal, this will enable shell completion

.. code-block::

    echo 'eval "$(_HCKR_COMPLETE=zsh_source hckr)"' >> ~/.zshrc

.. tip::
   ``hckr`` uses click's native shell completion functionality. refer following docs for more information `docs <https://click.palletsprojects.com/en/8.1.x/shell-completion/>`_.
