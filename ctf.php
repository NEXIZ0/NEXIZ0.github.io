<?php

function decrypt($encrypted, $key) {
    list($iv_base64, $ciphertext_base64) = explode(":", $encrypted);

    $iv = base64_decode($iv_base64);
    $ciphertext = base64_decode($ciphertext_base64);

    // Use the same encryption method as used for encryption
    $plaintext = openssl_decrypt($ciphertext, 'aes-256-cbc', $key, OPENSSL_RAW_DATA, $iv);

    return $plaintext;
}

// Encrypted string in the format "iv_base64:ciphertext_base64"
$encrypted_password = "YC7gGz0yO2n1nvhvN0AcDg==:AoiG3qxHiyRLUMYM1/NSfiCiqGIxtZJt5OQRl681TtM=";

// Path to the word list file
$word_list_file = 'rockyou-75.txt';

$correct_key = null;
$plaintext_password = null;

if (($handle = fopen($word_list_file, "r")) !== false) {
    while (($key = fgets($handle)) !== false) {
        $key = trim($key);

        $decrypted = decrypt($encrypted_password, $key);
        if ($decrypted !== false) {
            // Check if decrypted content is printable
            if (ctype_print($decrypted)) {
                $correct_key = $key;
                $plaintext_password = $decrypted;
                break;
            }
        }
    }
    fclose($handle);
}

if ($correct_key !== null) {
    echo "Correct Key: " . $correct_key . "\n";
    echo "Decrypted Password: " . $plaintext_password . "\n";
} else {
    echo "No valid password found with the given keys.\n";
}
?>
