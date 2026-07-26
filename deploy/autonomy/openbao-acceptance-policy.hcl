path "sys/health" {
  capabilities = ["read"]
}

path "transit/keys/workchord-server-acceptance" {
  capabilities = ["read"]
}

path "transit/sign/workchord-server-acceptance" {
  capabilities = ["update"]
}

path "transit/verify/workchord-server-acceptance" {
  capabilities = ["update"]
}
