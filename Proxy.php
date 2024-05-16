<?php
// Function to proxy the request
function proxyRequest($url) {
    // Initialize a cURL session
    $ch = curl_init();

    // Set the URL
    curl_setopt($ch, CURLOPT_URL, $url);

    // Set options to return the transfer as a string
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);

    // Optionally, follow redirects
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);

    // Execute the cURL request
    $response = curl_exec($ch);

    // Check for cURL errors
    if (curl_errno($ch)) {
        return "cURL error: " . curl_error($ch);
    }

    // Close the cURL session
    curl_close($ch);

    // Return the response
    return $response;
}

// Check if the URL parameter is provided
$url = isset($_GET['url']) ? filter_var($_GET['url'], FILTER_SANITIZE_URL) : '';

?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Simple PHP Proxy</title>
</head>
<body>
    <h1>Simple PHP Proxy</h1>
    <form method="get" action="">
        <label for="url">Enter URL:</label>
        <input type="text" id="url" name="url" required value="<?php echo htmlspecialchars($url); ?>">
        <button type="submit">Load Page</button>
    </form>

    <?php
    if ($url) {
        if (filter_var($url, FILTER_VALIDATE_URL)) {
            // Valid URL, proxy the request and display the response
            echo '<div>';
            echo proxyRequest($url);
            echo '</div>';
        } else {
            // Invalid URL
            echo '<p>Invalid URL</p>';
        }
    }
    ?>
</body>
</html>
