Shell Completion
=====================================
``hckr`` provides tab completion support for **Bash** (version 4.4 and up), **Zsh**.

.. tip::
   ``hckr`` uses click's native shell completion functionality.     refer following docs for more information `docs <https://click.palletsprojects.com/en/8.1.x/shell-completion/>`_.

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
