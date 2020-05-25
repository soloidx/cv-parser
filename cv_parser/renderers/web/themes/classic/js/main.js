let animation_engine = (function () {
  let header_timeline = gsap.timeline();
  let experience_timeline = gsap.timeline();
  let experience_started = false;
  let experience_animations = [];
  let animated_sections = [
    ".core_formation",
    ".complementary_formation",
    ".languages",
    ".skills",
    ".hobbies",
    ".events",
    ".references",
  ];

  let animate_header = function () {
    header_timeline.from("header>div.photo", { opacity: 0, duration: 2 });
    header_timeline.from("header>h1", { opacity: 0, y: 20, duration: 1 }, 1);
    header_timeline.from("header>h3", { opacity: 0, y: 20, duration: 1 }, 1.2);
    header_timeline.from("header>.headline", { opacity: 0, duration: 1 }, "-=0.5");
    header_timeline.from("header>address", { opacity: 0, duration: 2 }, "-=0.5");
  };

  let initialize_experiences = function () {
    let odd_experiences = document.querySelectorAll(
      ".experience>ul>li:nth-child(odd)"
    );
    let even_experiences = document.querySelectorAll(
      ".experience>ul>li:nth-child(even)"
    );

    for (let i = 0; i < odd_experiences.length; i++) {
      let work_ele = odd_experiences[i];
      let off = work_ele.offsetTop;
      experience_animations.push({
        element: work_ele,
        offset: off,
      });
      experience_timeline.set(work_ele.querySelector(".project"), {
        x: -20,
        opacity: 0,
      });
    }

    for (let i = 0; i < even_experiences.length; i++) {
      let work_ele = even_experiences[i];
      let off = work_ele.offsetTop;
      experience_animations.push({
        element: work_ele,
        offset: off,
      });
      experience_timeline.set(work_ele.querySelector(".project"), {
        x: 20,
        opacity: 0,
      });
    }

    experience_timeline.set("section.experience .section-title", { opacity: 0 });
    experience_timeline.set(".experience>ul>li", { opacity: 0 });
    experience_timeline.set("section.experience", { opacity: 1 });
  };

  let experience_on_scroll = function (offset) {
    let title_offset = document.querySelector("section.experience .section-title")
      .offsetTop;
    if (!experience_started && title_offset - offset <= 0) {
      experience_timeline.to("section.experience .section-title", {
        opacity: 1,
        duration: 1,
      });
      experience_started = true;
    }

    let i = experience_animations.length;
    while (i--) {
      let ele_offset = experience_animations[i].element.offsetTop;
      if (ele_offset - offset <= 0) {
        gsap.to(experience_animations[i].element, { opacity: 1, duration: 2 });
        let pro_ele = experience_animations[i].element.querySelector(
          ".project"
        );
        gsap.to(pro_ele, { x: 0, opacity: 1, duration: 1 });
        experience_animations.splice(i, 1);
      }
    }
  };

  let initialize_sections = function() {
    for(let i = 0; i < animated_sections.length; i++){
      gsap.set(animated_sections[i], {opacity: 0});
      gsap.set(animated_sections[i] + ">ul>li", {y: 10,opacity: 0});
    }
  }

  let sections_on_scroll = function (offset) {
    let i = animated_sections.length;
    while(i--){
      let section_ele = document.querySelector(animated_sections[i])
      let offset_ele = section_ele.offsetTop;
      if(offset_ele - offset <= 0 ){
        let tl = gsap.timeline();
        tl.to(section_ele, { opacity: 1, duration: 1.5 });
        document.querySelectorAll(animated_sections[i]+">ul>li").forEach((ele) => {
          tl.to(ele, { y: 0, opacity: 1, duration: 0.5 }, "-=0.3");
        });
        animated_sections.splice(i, 1)
      }
    }
  }

  let on_scroll = function (evt) {
    let main_offset = evt.target.scrollingElement.scrollTop;
    let window_height = document.defaultView.innerHeight;

    main_offset = main_offset + window_height / 1.2;

    let animation_blocks = [experience_on_scroll, sections_on_scroll];
    animation_blocks.forEach((func) => func(main_offset));
  };

  let initialize = function () {
    header_timeline.set("header", { opacity: 1 });
    animate_header();
    initialize_experiences();
    initialize_sections();
    document.addEventListener("scroll", on_scroll);
  };

  return {
    initialize: initialize,
  };
})();

document.addEventListener("DOMContentLoaded", (event) => {
  animation_engine.initialize();
});
