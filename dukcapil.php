<?php

$curl = curl_init();

curl_setopt_array($curl, array(
  CURLOPT_URL => 'http://prm.customs.go.id/Prm/dukcapil.html',
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => '',
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 0,
  CURLOPT_FOLLOWLOCATION => true,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => 'POST',
  CURLOPT_POSTFIELDS =>'content=list&noKK=&nik=&nama=anwar+ibrahim&tempatLahir=&tglLahir=&namaIbu=&provinsi=&kabupaten=&kecamatan=&kelurahan=&page=2',
  CURLOPT_HTTPHEADER => array(
    'User-Agent:  Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Accept:  */*',
    'Accept-Language:  en-US,en;q=0.5',
    'Accept-Encoding:  gzip, deflate',
    'Content-Type:  application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With:  XMLHttpRequest',
    'Origin:  http://prm.customs.go.id',
    'Connection:  keep-alive',
    'Referer:  http://prm.customs.go.id/Prm/',
    'Cookie:  JSESSIONID=976cfaac3b0f9fc916519baf1d65; BIGipServerPOOL_DJBC_PRM_INHOUSE=2047058186.45933.0000'
  ),
));

$response = curl_exec($curl);

curl_close($curl);
// echo $response;

$matches = [];
$foundMatch = preg_match_all('%<td class="urut">(\d+)</td><td>(\d+)</td><td class="nik"><strong><a style=\"cursor: pointer;\">(\d+)</a></strong></td><td>([\w\.\,\s]+)</td><td>([\w\s\.\,]+)</td><td>(\d{4}\-\d{2}\-\d{2})</td><td>([\w\s\.\,]+)</td><td>([\w\s\.\,]+)</td><td>([\w\s\.\,]+)</td><td>([\w\s\.\,]+)</td><td>([\w\s\.\,]+)</td>%si', $response, $matches);

if (!$foundMatch) {
  die("Cookies invalid. Please refresh the cookie.");
}
// var_dump($matches);

// check if length is 12
if (count($matches) < 12) {
  die("No matching data found, or request is error");
}

// otherwise, pack into json?
// print_r($matches);
$dataCount = count($matches[0]);
if (strlen($matches[0][0]) < 1 ) {
  die("No data found.");
}

// iterate over the matches, skip the 1st column
$data = [];
for ($i = 0; $i < $dataCount; ++$i) {
  $urut = $matches[1][$i];
  $noKK = $matches[2][$i];
  $nik = $matches[3][$i];
  $nama = $matches[4][$i];
  $kotaLahir = $matches[5][$i];
  $tglLahir = $matches[6][$i];
  $alamat = $matches[7][$i];
  $propinsi = $matches[8][$i];
  $kota = $matches[9][$i];
  $kecamatan = $matches[10][$i];
  $kelurahan = $matches[11][$i];

  $data[] = [
    'urut' => $urut,
    'noKK' => $noKK,
    'nik' => $nik,
    'nama' => $nama,
    'kotaLahir' => $kotaLahir,
    'tglLahir' => $tglLahir,
    'alamat' => $alamat,
    'propinsi' => $propinsi,
    'kota' => $kota,
    'kecamatan' => $kecamatan,
    'kelurahan' => $kelurahan,
  ];
}

echo json_encode($data);