:orphan:

MATLAB provides shortcuts to plot ERD of a table neighborhood or a schema using the ``erd`` command:

.. code-block:: matlab

    % plot the ERD of the stimulus schema
    erd stimulus

    % plot the neighborhood of the stimulus.Trial table
    erd stimulus.Trial

    % plot the stimulus and experiment schemas and the neighborhood of preprocess.Sync
    erd stimulus experiment preprocess.Sync

