def update_record(session, record, new_values):
    # Update the record's fields with the new values
    for field, new_value in new_values.items():
        setattr(record, field, new_value)

    # Increment the version field
    record.version += 1

    # Commit the changes
    session.commit()