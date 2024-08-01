<?php

function decrypt($encrypted, $key) {
    list($iv_base64, $ciphertext_base64) = explode(":", $encrypted);

    $iv = base64_decode($iv_base64);
    $ciphertext = base64_decode($ciphertext_base64);

    $plaintext = openssl_decrypt($ciphertext, 'aes-256-cbc', $key, OPENSSL_RAW_DATA, $iv);

    return $plaintext;
}

// Example encrypted string in the format "iv_base64:ciphertext_base64"
$encrypted_password = "your_iv_base64:your_ciphertext_base64";

// Path to the word list file
$word_list_file = 'path/to/your/wordlist.txt';

$plaintext_password = null;

// Open the word list file
if (($handle = fopen($word_list_file, "r")) !== false) {
    while (($key = fgets($handle)) !== false) {
        // Remove any whitespace or newline characters
        $key = trim($key);

        $decrypted = decrypt($encrypted_password, $key);
        if ($decrypted !== false) {
            $plaintext_password = $decrypted;
            echo "Password found: " . $plaintext_password . "\n";
            break;
        }
    }
    fclose($handle);
}

if ($plaintext_password === null) {
    echo "No valid password found with the given keys.\n";
}
?>
