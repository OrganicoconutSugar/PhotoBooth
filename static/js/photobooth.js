window.addEventListener('DOMContentLoaded', () => {
    // Animasi GSAP halus saat komponen masuk layar
    gsap.from('.chamber-viewport', { opacity: 0, y: 20, duration: 1, ease: "power3.out" });
    gsap.from('.panel-card', { opacity: 0, y: 20, duration: 1, stagger: 0.1, ease: "power3.out" });

    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    const smileStatus = document.getElementById('smile-status');
    const cameraStatus = document.getElementById('camera-status');
    const smileBar = document.getElementById('smile-bar');
    const smileBadgePercent = document.getElementById('smile-badge-percent');
    const captureBtn = document.getElementById('capture-btn');
    const countdownOverlay = document.getElementById('countdown-overlay');
    const countdownText = document.getElementById('countdown-text');

    let isCountdownActive = false;
    let isCapturing = false;
    let currentSmileScore = 0;

    video.addEventListener('loadedmetadata', () => {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        cameraStatus.innerHTML = '<span class="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-ping"></span> <span class="text-emerald-600 font-bold">Aktif</span>';
    });

    function cDistance(p1, p2) {
        return Math.sqrt(Math.pow(p1.x - p2.x, 2) + Math.pow(p1.y - p2.y, 2));
    }

    function detectSmile(landmarks) {
        const mouthLeft = landmarks[61];
        const mouthRight = landmarks[291];
        const faceLeft = landmarks[234];
        const faceRight = landmarks[454];

        const mouthWidth = cDistance(mouthLeft, mouthRight);
        const faceWidth = cDistance(faceLeft, faceRight);
        const normalizedRatio = mouthWidth / (faceWidth + 0.0001);

        let smileScore = Math.round((normalizedRatio - 0.34) * 1250);
        if (smileScore < 0) smileScore = 0;
        if (smileScore > 100) smileScore = 100;

        return smileScore;
    }

    function executeShutter() {
        isCapturing = true;
        countdownOverlay.style.opacity = "0";
        smileStatus.innerHTML = '<span class="text-amber-600 animate-pulse">Mengambil foto...</span>';

        const captureCanvas = document.createElement('canvas');
        captureCanvas.width = video.videoWidth;
        captureCanvas.height = video.videoHeight;
        const cCtx = captureCanvas.getContext('2d');

        cCtx.translate(captureCanvas.width, 0);
        cCtx.scale(-1, 1);
        cCtx.drawImage(video, 0, 0, captureCanvas.width, captureCanvas.height);

        const dataUrl = captureCanvas.toDataURL('image/jpeg');

        fetch('/save-photo', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: dataUrl, smile_score: currentSmileScore })
        })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    smileStatus.innerHTML = '<span class="text-emerald-600">Tersimpan</span>';
                } else {
                    smileStatus.innerHTML = '<span class="text-emerald-600">Foto diambil</span>';
                }
                setTimeout(() => { isCapturing = false; isCountdownActive = false; }, 2000);
            })
            .catch(err => {
                console.error(err);
                smileStatus.innerHTML = '<span class="text-emerald-600">Foto diambil</span>';
                setTimeout(() => { isCapturing = false; isCountdownActive = false; }, 1500);
            });
    }

    function startCountdown() {
        isCountdownActive = true;
        countdownOverlay.classList.remove('pointer-events-none');
        countdownOverlay.style.opacity = "1";

        let currentCount = 5;
        countdownText.innerText = currentCount;
        countdownText.style.transform = "scale(1)";

        const interval = setInterval(() => {
            currentCount--;
            if (currentCount >= 1) {
                countdownText.innerText = currentCount;
                countdownText.style.transform = "scale(1.1)";
                setTimeout(() => { countdownText.style.transform = "scale(1)"; }, 150);
            } else {
                clearInterval(interval);
                countdownOverlay.classList.add('pointer-events-none');
                countdownOverlay.style.opacity = "0";
                executeShutter();
            }
        }, 1000);
    }

    captureBtn.addEventListener('click', () => {
        if (!isCountdownActive && !isCapturing) {
            startCountdown();
        }
    });

    const FaceMeshClass = window.FaceMesh || (typeof FaceMesh !== 'undefined' ? FaceMesh : null);
    if (!FaceMeshClass) {
        console.error("MediaPipe FaceMesh library not loaded!");
        smileStatus.innerHTML = '<span class="text-red-500 font-bold">Deteksi wajah gagal dimuat</span>';
        return;
    }

    const faceMesh = new FaceMeshClass({
        locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh@0.4/${file}`
    });

    faceMesh.setOptions({
        maxNumFaces: 1,
        refineLandmarks: true,
        minDetectionConfidence: 0.5,
        minTrackingConfidence: 0.5
    });

    faceMesh.onResults((results) => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        if (results.multiFaceLandmarks && results.multiFaceLandmarks.length > 0) {
            const landmarks = results.multiFaceLandmarks[0];
            const score = detectSmile(landmarks);
            currentSmileScore = score;

            if (!isCountdownActive && !isCapturing) {
                smileStatus.innerHTML = `Senyum: <span class="text-zinc-900 font-black">${score}%</span>`;
                smileBar.style.width = `${score}%`;
                smileBadgePercent.innerText = `${score}%`;

                if (score >= 80) {
                    startCountdown();
                }
            }

            ctx.fillStyle = "rgba(16, 185, 129, 0.4)";
            for (const landmark of landmarks) {
                ctx.fillRect(landmark.x * canvas.width, landmark.y * canvas.height, 1.2, 1.2);
            }
        } else {
            if (!isCountdownActive && !isCapturing) {
                smileStatus.innerHTML = '<span class="text-zinc-400 font-bold">Siap</span>';
                currentSmileScore = 0;
                smileBar.style.width = `0%`;
                smileBadgePercent.innerText = `0%`;
            }
        }
    });

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
            video.play();

            const CameraClass = window.Camera || (typeof Camera !== 'undefined' ? Camera : null);
            if (CameraClass) {
                const camera = new CameraClass(video, {
                    onFrame: async () => {
                        await faceMesh.send({ image: video });
                    },
                    width: 640,
                    height: 480
                });
                camera.start();
            } else {
                console.warn("MediaPipe Camera utility not loaded. Using requestAnimationFrame fallback.");
                
                const processFrame = async () => {
                    if (!video.paused && !video.ended) {
                        try {
                            await faceMesh.send({ image: video });
                        } catch (e) {
                            console.error("Error processing frame: ", e);
                        }
                    }
                    requestAnimationFrame(processFrame);
                };
                
                video.addEventListener('loadeddata', () => {
                    processFrame();
                });
            }
        })
        .catch(err => {
            console.error(err);
            smileStatus.innerHTML = '<span class="text-red-500">Kamera tidak bisa dibuka</span>';
        });
});
