function ErrorMessage({ error }) {
  if (!error) {
    return null;
  }

  return (
    <div className="error-message" role="alert">

      <div className="error-icon">
        !
      </div>

      <div>

        <strong>
          Something went wrong
        </strong>

        <p>
          {error}
        </p>

      </div>

    </div>
  );
}

export default ErrorMessage;
