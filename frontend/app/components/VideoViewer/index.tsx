"use client";
import React, { useMemo } from "react";
import YouTube from "react-youtube";
import "./VideoViewer.css";

interface Props {
	videoLink: string;
}

const VideoViewer = ({ videoLink }: Props) => {
	function extractYouTubeId(url: string) {
		const regex1 =
			/^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
		const regex2 = /^.*((m\.)?youtube\.com)\/.*((\?v=)|(\/v\/))([^\/]+)/;
		let match = url.match(regex1);
		if (match && match[2].length == 11) {
			return match[2];
		} else {
			match = url.match(regex2);
			if (match && match[5].length == 11) {
				return match[5];
			}
		}
		return null;
	}

	const videoIdFunc = extractYouTubeId(videoLink);

	const videoId = useMemo(() => {
		const splitWithWatch = videoLink?.split("/watch?");
		if (splitWithWatch?.length === 2) {
			const vParamSemi = splitWithWatch[1]
				.split("&")
				.find((elem) => elem.startsWith("v="));
			if (vParamSemi) {
				const vParamDone = vParamSemi.split("v=")[1];
				return vParamDone;
			}
		} else {
		}
	}, [videoLink]);

	const opts = {
		height: "390",
		width: "640",
		playerVars: {
			// https://developers.google.com/youtube/player_parameters
			autoplay: 1,
		},
	};

	const onReady = (event: any) => {
		// access to player in all event handlers via event.target
		event.target.pauseVideo();
	};

	return (
		<div className="video-container">
			<YouTube videoId={videoId} opts={opts} onReady={onReady} />
		</div>
	);
};

export default VideoViewer;
